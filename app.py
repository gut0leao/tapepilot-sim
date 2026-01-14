import sys
import time
import math
from dataclasses import dataclass

import numpy as np
import pyqtgraph as pg

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QSlider, QLabel, QGraphicsView, QGraphicsScene
)
from PySide6.QtSvgWidgets import QGraphicsSvgItem


# -----------------------------
# Simulação (bem simples, só para provar o loop + UI)
# -----------------------------
@dataclass
class SimState:
    transport: str = "STOP"     # STOP/PLAY/FF/REW/PAUSE
    rpm_setpoint: float = 0.0
    rpm: float = 0.0
    pwm: float = 0.0
    err: float = 0.0
    tension: float = 0.0

    # "falhas" (sliders)
    tape_friction: float = 0.0      # 0..1
    encoder_jitter: float = 0.0     # 0..1

    # ângulos visuais (graus)
    reel_l_deg: float = 0.0
    reel_r_deg: float = 0.0
    capstan_deg: float = 0.0


class Simulator:
    """
    Simulador mínimo:
    - PLAY: setpoint ~ 1800 rpm (exemplo)
    - STOP: setpoint 0
    - Dinâmica simplificada: rpm segue setpoint com 1ª ordem + atrito
    - pwm fictício = clamp(err * Kp)
    """
    def __init__(self):
        self.s = SimState()
        self.Kp = 0.02
        self.tau = 0.25  # constante de tempo (s)

    def set_transport(self, mode: str):
        self.s.transport = mode

    def step(self, dt: float):
        # setpoints por modo
        if self.s.transport == "PLAY":
            self.s.rpm_setpoint = 1800.0
        elif self.s.transport == "FF":
            self.s.rpm_setpoint = 2600.0
        elif self.s.transport == "REW":
            self.s.rpm_setpoint = 2600.0
        elif self.s.transport == "PAUSE":
            self.s.rpm_setpoint = 300.0
        else:
            self.s.rpm_setpoint = 0.0

        # erro e "pwm" (controle fictício)
        self.s.err = self.s.rpm_setpoint - self.s.rpm
        pwm = self.Kp * self.s.err
        pwm = max(min(pwm, 1.0), -1.0)
        self.s.pwm = pwm

        # atrito e "tensão" simulada
        friction_load = self.s.tape_friction * 600.0  # rpm "equivalente" de carga
        self.s.tension = self.s.tape_friction * (0.3 + 0.7 * abs(self.s.pwm))

        # dinâmica 1ª ordem (bem simples)
        target = self.s.rpm_setpoint - friction_load * abs(self.s.pwm)
        target = max(target, 0.0)

        alpha = dt / (self.tau + dt)
        self.s.rpm = (1 - alpha) * self.s.rpm + alpha * target

        # encoder jitter (só para demonstrar efeito visual)
        jitter = (np.random.randn() * self.s.encoder_jitter * 20.0)
        rpm_for_visual = max(self.s.rpm + jitter, 0.0)

        # converter rpm -> rad/s
        omega = (rpm_for_visual * 2 * math.pi) / 60.0

        # atualizar ângulos (graus)
        self.s.capstan_deg = (self.s.capstan_deg + math.degrees(omega * dt)) % 360.0
        # reels: velocidades proporcionais (só “pra ver” rodar)
        self.s.reel_l_deg = (self.s.reel_l_deg + math.degrees(0.6 * omega * dt)) % 360.0
        self.s.reel_r_deg = (self.s.reel_r_deg + math.degrees(0.9 * omega * dt)) % 360.0

        return self.s


# -----------------------------
# UI: Cena SVG + Controles + Gráficos
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TapePilot V1 - Simulador (WSL/Qt/SVG)")

        self.sim = Simulator()

        # ---------- Layout base ----------
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)

        top = QHBoxLayout()
        main.addLayout(top, 2)

        bottom = QHBoxLayout()
        main.addLayout(bottom, 1)

        # ---------- Mecânica (SVG em QGraphicsScene) ----------
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints() | self.view.renderHints())
        self.view.setMinimumHeight(360)
        top.addWidget(self.view, 2)

        # Carregar SVGs
        self.reel_l = QGraphicsSvgItem("assets/svg/reel_left.svg")
        self.reel_r = QGraphicsSvgItem("assets/svg/reel_right.svg")
        self.capstan = QGraphicsSvgItem("assets/svg/capstan.svg")

        # Adicionar na cena
        self.scene.addItem(self.reel_l)
        self.scene.addItem(self.reel_r)
        self.scene.addItem(self.capstan)

        # Posicionar (ajuste conforme os teus SVGs)
        self.reel_l.setPos(60, 60)
        self.reel_r.setPos(300, 60)
        self.capstan.setPos(200, 200)

        # Pivô de rotação = centro do boundingRect do item
        for item in (self.reel_l, self.reel_r, self.capstan):
            pivot = item.boundingRect().center()
            item.setTransformOriginPoint(pivot)

        # ---------- Painel de controlo ----------
        panel = QVBoxLayout()
        top.addLayout(panel, 1)

        # Botões transporte
        btns = QGridLayout()
        panel.addLayout(btns)

        self.btn_stop = QPushButton("STOP")
        self.btn_play = QPushButton("PLAY")
        self.btn_ff = QPushButton("FF")
        self.btn_rew = QPushButton("REW")
        self.btn_pause = QPushButton("PAUSE")

        btns.addWidget(self.btn_stop, 0, 0)
        btns.addWidget(self.btn_play, 0, 1)
        btns.addWidget(self.btn_ff, 1, 0)
        btns.addWidget(self.btn_rew, 1, 1)
        btns.addWidget(self.btn_pause, 2, 0, 1, 2)

        self.btn_stop.clicked.connect(lambda: self.sim.set_transport("STOP"))
        self.btn_play.clicked.connect(lambda: self.sim.set_transport("PLAY"))
        self.btn_ff.clicked.connect(lambda: self.sim.set_transport("FF"))
        self.btn_rew.clicked.connect(lambda: self.sim.set_transport("REW"))
        self.btn_pause.clicked.connect(lambda: self.sim.set_transport("PAUSE"))

        panel.addSpacing(10)

        # Sliders de falhas
        panel.addWidget(QLabel("Falhas (em tempo real)"))

        self.sl_friction = QSlider(Qt.Horizontal)
        self.sl_friction.setRange(0, 100)
        self.sl_friction.setValue(0)
        panel.addWidget(QLabel("Atrito da fita"))
        panel.addWidget(self.sl_friction)

        self.sl_jitter = QSlider(Qt.Horizontal)
        self.sl_jitter.setRange(0, 100)
        self.sl_jitter.setValue(0)
        panel.addWidget(QLabel("Jitter do encoder"))
        panel.addWidget(self.sl_jitter)

        panel.addSpacing(10)

        # “Telemetria”
        self.lbl = QLabel("—")
        self.lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        panel.addWidget(self.lbl)
        panel.addStretch(1)

        # ---------- Gráficos (pyqtgraph) ----------
        pg.setConfigOptions(antialias=True)

        self.plot_rpm = pg.PlotWidget(title="RPM (setpoint vs medido)")
        self.plot_pwm = pg.PlotWidget(title="PWM / Comando")
        self.plot_err = pg.PlotWidget(title="Erro")
        self.plot_tension = pg.PlotWidget(title="Tensão (simulada)")

        bottom.addWidget(self.plot_rpm, 2)
        bottom.addWidget(self.plot_pwm, 1)
        bottom.addWidget(self.plot_err, 1)
        bottom.addWidget(self.plot_tension, 1)

        self.cur_rpm_sp = self.plot_rpm.plot([], [])
        self.cur_rpm = self.plot_rpm.plot([], [])
        self.cur_pwm = self.plot_pwm.plot([], [])
        self.cur_err = self.plot_err.plot([], [])
        self.cur_tension = self.plot_tension.plot([], [])

        # Buffers
        self.t0 = time.time()
        self.window_s = 20.0
        self.ts = []
        self.rpm_sp = []
        self.rpm = []
        self.pwm = []
        self.err = []
        self.tension = []

        # Timer de simulação
        self.last = time.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS UI (sim também, por enquanto)

    def tick(self):
        now = time.time()
        dt = now - self.last
        self.last = now

        # ler sliders
        self.sim.s.tape_friction = self.sl_friction.value() / 100.0
        self.sim.s.encoder_jitter = self.sl_jitter.value() / 100.0

        # simular
        s = self.sim.step(dt)

        # atualizar SVGs (rotação)
        self.reel_l.setRotation(s.reel_l_deg)
        self.reel_r.setRotation(s.reel_r_deg)
        self.capstan.setRotation(s.capstan_deg)

        # telemetria
        self.lbl.setText(
            f"Transport: {s.transport}\n"
            f"RPM: {s.rpm:7.1f} | Set: {s.rpm_setpoint:7.1f}\n"
            f"PWM: {s.pwm:+.3f} | Err: {s.err:+.1f}\n"
            f"Atrito: {s.tape_friction:.2f} | Jitter: {s.encoder_jitter:.2f}\n"
            f"Tensão: {s.tension:.3f}"
        )

        # buffers (janela deslizante)
        t = now - self.t0
        self.ts.append(t)
        self.rpm_sp.append(s.rpm_setpoint)
        self.rpm.append(s.rpm)
        self.pwm.append(s.pwm)
        self.err.append(s.err)
        self.tension.append(s.tension)

        # cortar para últimos N segundos
        while self.ts and (self.ts[-1] - self.ts[0]) > self.window_s:
            self.ts.pop(0)
            self.rpm_sp.pop(0)
            self.rpm.pop(0)
            self.pwm.pop(0)
            self.err.pop(0)
            self.tension.pop(0)

        # atualizar plots
        self.cur_rpm_sp.setData(self.ts, self.rpm_sp)
        self.cur_rpm.setData(self.ts, self.rpm)
        self.cur_pwm.setData(self.ts, self.pwm)
        self.cur_err.setData(self.ts, self.err)
        self.cur_tension.setData(self.ts, self.tension)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
