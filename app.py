import sys
import time

import pyqtgraph as pg

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QSlider, QLabel, QGraphicsView, QGraphicsScene,
    QCheckBox
)
from PySide6.QtSvgWidgets import QGraphicsSvgItem

from sim import Simulator


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

        # Os SVGs foram exportados com 800 x 800 px. Exibi-los no tamanho
        # original faz com que ocupem praticamente toda a cena, portanto cada
        # componente recebe uma largura visual adequada, mantendo a proporção.
        def set_svg_width(item, width):
            original_width = item.boundingRect().width()
            if original_width > 0:
                item.setScale(width / original_width)

        set_svg_width(self.reel_l, 180)
        set_svg_width(self.reel_r, 180)
        set_svg_width(self.capstan, 70)

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

        panel.addWidget(QLabel("Wow / Flutter"))

        self.wow_enabled = QCheckBox("Wow ativo")
        self.wow_frequency = QSlider(Qt.Horizontal)
        self.wow_frequency.setRange(1, 20)
        self.wow_frequency.setValue(5)
        self.wow_frequency_value = QLabel()
        self.wow_amplitude = QSlider(Qt.Horizontal)
        self.wow_amplitude.setRange(0, 300)
        self.wow_amplitude.setValue(100)
        self.wow_amplitude_value = QLabel()
        panel.addWidget(self.wow_enabled)
        panel.addWidget(QLabel("Taxa característica do wow"))
        panel.addWidget(self.wow_frequency)
        panel.addWidget(self.wow_frequency_value)
        panel.addWidget(QLabel("Intensidade do wow — Dry ↔ Wet"))
        panel.addWidget(self.wow_amplitude)
        panel.addWidget(self.wow_amplitude_value)

        self.flutter_enabled = QCheckBox("Flutter ativo")
        self.flutter_frequency = QSlider(Qt.Horizontal)
        self.flutter_frequency.setRange(20, 200)
        self.flutter_frequency.setValue(80)
        self.flutter_frequency_value = QLabel()
        self.flutter_amplitude = QSlider(Qt.Horizontal)
        self.flutter_amplitude.setRange(0, 100)
        self.flutter_amplitude.setValue(30)
        self.flutter_amplitude_value = QLabel()
        panel.addWidget(self.flutter_enabled)
        panel.addWidget(QLabel("Taxa característica do flutter"))
        panel.addWidget(self.flutter_frequency)
        panel.addWidget(self.flutter_frequency_value)
        panel.addWidget(QLabel("Intensidade do flutter — Dry ↔ Wet"))
        panel.addWidget(self.flutter_amplitude)
        panel.addWidget(self.flutter_amplitude_value)

        self.wow_frequency.valueChanged.connect(self.update_disturbance_labels)
        self.wow_amplitude.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_frequency.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_amplitude.valueChanged.connect(self.update_disturbance_labels)
        self.update_disturbance_labels()

        self.btn_restore_disturbances = QPushButton("Restaurar padrão")
        panel.addWidget(self.btn_restore_disturbances)
        self.btn_restore_disturbances.clicked.connect(self.restore_disturbances)

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
        self.t0 = time.monotonic()
        self.window_s = 20.0
        self.ts = []
        self.rpm_sp = []
        self.rpm = []
        self.pwm = []
        self.err = []
        self.tension = []

        # Timer de simulação
        self.last = time.monotonic()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS UI (sim também, por enquanto)

    def restore_disturbances(self):
        self.wow_enabled.setChecked(False)
        self.wow_frequency.setValue(5)
        self.wow_amplitude.setValue(100)
        self.flutter_enabled.setChecked(False)
        self.flutter_frequency.setValue(80)
        self.flutter_amplitude.setValue(30)

    def update_disturbance_labels(self, _value=None):
        self.wow_frequency_value.setText(
            f"{self.wow_frequency.value() / 10.0:.1f} Hz"
        )
        self.wow_amplitude_value.setText(
            f"Dry {self.wow_amplitude.value() / 100.0:.2f}% Wet"
        )
        self.flutter_frequency_value.setText(
            f"{self.flutter_frequency.value() / 10.0:.1f} Hz"
        )
        self.flutter_amplitude_value.setText(
            f"Dry {self.flutter_amplitude.value() / 100.0:.2f}% Wet"
        )

    def tick(self):
        now = time.monotonic()
        dt = now - self.last
        self.last = now

        # ler sliders
        self.sim.s.tape_friction = self.sl_friction.value() / 100.0
        self.sim.s.encoder_jitter = self.sl_jitter.value() / 100.0
        disturbances = self.sim.faults.disturbances
        disturbances.wow.enabled = self.wow_enabled.isChecked()
        disturbances.wow.set_frequency(self.wow_frequency.value() / 10.0)
        disturbances.wow.set_amplitude(self.wow_amplitude.value() / 10000.0)
        disturbances.flutter.enabled = self.flutter_enabled.isChecked()
        disturbances.flutter.set_frequency(self.flutter_frequency.value() / 10.0)
        disturbances.flutter.set_amplitude(
            self.flutter_amplitude.value() / 10000.0
        )

        # simular
        s = self.sim.advance(dt)

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
            f"Wow: {s.wow_disturbance * 100:+.2f}% | "
            f"Flutter: {s.flutter_disturbance * 100:+.2f}%\n"
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
