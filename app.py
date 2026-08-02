import sys
import time

import pyqtgraph as pg

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QSlider, QLabel, QGraphicsView, QGraphicsScene,
    QScrollArea, QCheckBox
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

        # Telemetria fixa, visível acima da cena mecânica e dos gráficos.
        self.lbl = QLabel("—")
        self.lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main.addWidget(self.lbl)

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
        panel_widget = QWidget()
        panel = QVBoxLayout(panel_widget)
        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setWidget(panel_widget)
        top.addWidget(panel_scroll, 1)

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

        self.chk_digital_tach = QCheckBox("Digital Tach ON")
        panel.addWidget(self.chk_digital_tach)

        self.pid_kp = QSlider(Qt.Horizontal)
        self.pid_kp.setRange(0, 5000)
        self.pid_kp.setValue(1000)
        self.pid_kp_value = QLabel()
        panel.addWidget(QLabel("PID — Kp"))
        panel.addWidget(self.pid_kp)
        panel.addWidget(self.pid_kp_value)

        self.pid_ki = QSlider(Qt.Horizontal)
        self.pid_ki.setRange(0, 10000)
        self.pid_ki.setValue(2000)
        self.pid_ki_value = QLabel()
        panel.addWidget(QLabel("PID — Ki"))
        panel.addWidget(self.pid_ki)
        panel.addWidget(self.pid_ki_value)

        self.pid_kd = QSlider(Qt.Horizontal)
        self.pid_kd.setRange(0, 1000)
        self.pid_kd.setValue(0)
        self.pid_kd_value = QLabel()
        panel.addWidget(QLabel("PID — Kd"))
        panel.addWidget(self.pid_kd)
        panel.addWidget(self.pid_kd_value)

        for slider in (self.pid_kp, self.pid_ki, self.pid_kd):
            slider.valueChanged.connect(self.update_pid_labels)
        self.update_pid_labels()

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

        self.sl_pulse_loss = QSlider(Qt.Horizontal)
        self.sl_pulse_loss.setRange(0, 100)
        self.sl_pulse_loss.setValue(0)
        panel.addWidget(QLabel("Perda de pulsos do encoder"))
        panel.addWidget(self.sl_pulse_loss)

        self.chk_encoder_dropout = QCheckBox("Dropout do encoder")
        panel.addWidget(self.chk_encoder_dropout)

        panel.addWidget(QLabel("Wow / Flutter"))

        self.wow_frequency = QSlider(Qt.Horizontal)
        self.wow_frequency.setRange(1, 20)
        self.wow_frequency.setValue(5)
        self.wow_frequency_value = QLabel()
        self.wow_amplitude = QSlider(Qt.Horizontal)
        self.wow_amplitude.setRange(0, 300)
        self.wow_amplitude.setValue(100)
        self.wow_amplitude_value = QLabel()
        self.wow_occurrence = QSlider(Qt.Horizontal)
        self.wow_occurrence.setRange(0, 100)
        self.wow_occurrence.setValue(0)
        self.wow_occurrence_value = QLabel()
        self.wow_duration = QSlider(Qt.Horizontal)
        self.wow_duration.setRange(5, 100)
        self.wow_duration.setValue(30)
        self.wow_duration_value = QLabel()
        panel.addWidget(QLabel("Taxa característica do wow"))
        panel.addWidget(self.wow_frequency)
        panel.addWidget(self.wow_frequency_value)
        panel.addWidget(QLabel("Intensidade do wow — Dry ↔ Wet"))
        panel.addWidget(self.wow_amplitude)
        panel.addWidget(self.wow_amplitude_value)
        panel.addWidget(QLabel("Ocorrência média do wow"))
        panel.addWidget(self.wow_occurrence)
        panel.addWidget(self.wow_occurrence_value)
        panel.addWidget(QLabel("Duração média do wow"))
        panel.addWidget(self.wow_duration)
        panel.addWidget(self.wow_duration_value)

        self.flutter_frequency = QSlider(Qt.Horizontal)
        self.flutter_frequency.setRange(20, 200)
        self.flutter_frequency.setValue(80)
        self.flutter_frequency_value = QLabel()
        self.flutter_amplitude = QSlider(Qt.Horizontal)
        self.flutter_amplitude.setRange(0, 100)
        self.flutter_amplitude.setValue(30)
        self.flutter_amplitude_value = QLabel()
        self.flutter_occurrence = QSlider(Qt.Horizontal)
        self.flutter_occurrence.setRange(0, 100)
        self.flutter_occurrence.setValue(0)
        self.flutter_occurrence_value = QLabel()
        self.flutter_duration = QSlider(Qt.Horizontal)
        self.flutter_duration.setRange(1, 30)
        self.flutter_duration.setValue(5)
        self.flutter_duration_value = QLabel()
        panel.addWidget(QLabel("Taxa característica do flutter"))
        panel.addWidget(self.flutter_frequency)
        panel.addWidget(self.flutter_frequency_value)
        panel.addWidget(QLabel("Intensidade do flutter — Dry ↔ Wet"))
        panel.addWidget(self.flutter_amplitude)
        panel.addWidget(self.flutter_amplitude_value)
        panel.addWidget(QLabel("Ocorrência média do flutter"))
        panel.addWidget(self.flutter_occurrence)
        panel.addWidget(self.flutter_occurrence_value)
        panel.addWidget(QLabel("Duração média do flutter"))
        panel.addWidget(self.flutter_duration)
        panel.addWidget(self.flutter_duration_value)

        self.wow_frequency.valueChanged.connect(self.update_disturbance_labels)
        self.wow_amplitude.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_frequency.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_amplitude.valueChanged.connect(self.update_disturbance_labels)
        self.wow_occurrence.valueChanged.connect(self.update_disturbance_labels)
        self.wow_duration.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_occurrence.valueChanged.connect(self.update_disturbance_labels)
        self.flutter_duration.valueChanged.connect(self.update_disturbance_labels)
        self.update_disturbance_labels()

        self.btn_restore_disturbances = QPushButton("Restaurar padrão")
        panel.addWidget(self.btn_restore_disturbances)
        self.btn_restore_disturbances.clicked.connect(self.restore_disturbances)

        panel.addSpacing(10)

        panel.addStretch(1)

        # ---------- Gráficos (pyqtgraph) ----------
        pg.setConfigOptions(antialias=True)

        self.plot_rpm = pg.PlotWidget(title="RPM (setpoint, física e encoder)")
        self.plot_pwm = pg.PlotWidget(title="PWM / Comando")
        self.plot_err = pg.PlotWidget(title="Erro")
        self.plot_tension = pg.PlotWidget(title="Tensão (simulada)")
        self.plot_rms = pg.PlotWidget(title="Erro RMS móvel (%)")

        bottom.addWidget(self.plot_rpm, 2)
        bottom.addWidget(self.plot_pwm, 1)
        bottom.addWidget(self.plot_err, 1)
        bottom.addWidget(self.plot_tension, 1)
        bottom.addWidget(self.plot_rms, 1)

        self.plot_rpm.addLegend()
        self.cur_rpm_sp = self.plot_rpm.plot(
            [], [],
            pen=pg.mkPen("#bd93f9", width=2),
            name="Setpoint",
        )
        self.cur_rpm = self.plot_rpm.plot(
            [], [], pen=pg.mkPen("#50fa7b", width=2), name="RPM física"
        )
        self.cur_encoder_rpm = self.plot_rpm.plot(
            [], [], pen=pg.mkPen("#8be9fd", width=2), name="Encoder filtrado"
        )
        self.cur_encoder_rpm_raw = self.plot_rpm.plot(
            [], [], pen=pg.mkPen("#ffb86c", width=1), name="Encoder bruto"
        )
        self.plot_pwm.addLegend()
        self.cur_pwm = self.plot_pwm.plot(
            [], [], pen=pg.mkPen("#50fa7b", width=2), name="Aplicado"
        )
        self.cur_pwm_requested = self.plot_pwm.plot(
            [], [], pen=pg.mkPen("#ff79c6", width=1), name="Solicitado"
        )
        self.cur_err = self.plot_err.plot([], [])
        self.cur_tension = self.plot_tension.plot([], [])
        self.cur_rms = self.plot_rms.plot(
            [], [], pen=pg.mkPen("#8be9fd", width=2)
        )
        self.plot_rms.addItem(
            pg.InfiniteLine(pos=0.1, angle=0, pen=pg.mkPen("#50fa7b", width=1))
        )
        self.plot_rms.addItem(
            pg.InfiniteLine(pos=0.2, angle=0, pen=pg.mkPen("#ff5555", width=1))
        )

        # Buffers
        self.t0 = time.monotonic()
        self.window_s = 20.0
        self.ts = []
        self.rpm_sp = []
        self.rpm = []
        self.encoder_rpm = []
        self.encoder_rpm_raw = []
        self.pwm = []
        self.pwm_requested = []
        self.err = []
        self.tension = []
        self.rms_ts = []
        self.rms_percent = []

        # Timer de simulação
        self.last = time.monotonic()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)  # ~60 FPS UI (sim também, por enquanto)

    def restore_disturbances(self):
        self.wow_frequency.setValue(5)
        self.wow_amplitude.setValue(100)
        self.wow_occurrence.setValue(0)
        self.wow_duration.setValue(30)
        self.flutter_frequency.setValue(80)
        self.flutter_amplitude.setValue(30)
        self.flutter_occurrence.setValue(0)
        self.flutter_duration.setValue(5)

    def update_pid_labels(self, _value=None):
        self.pid_kp_value.setText(f"{self.pid_kp.value() / 1_000_000:.6f}")
        self.pid_ki_value.setText(f"{self.pid_ki.value() / 1_000_000:.6f}")
        self.pid_kd_value.setText(f"{self.pid_kd.value() / 1_000_000:.6f}")

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
        self.wow_occurrence_value.setText(f"{self.wow_occurrence.value()}% do tempo")
        self.wow_duration_value.setText(f"{self.wow_duration.value() / 10.0:.1f} s")
        self.flutter_occurrence_value.setText(
            f"{self.flutter_occurrence.value()}% do tempo"
        )
        self.flutter_duration_value.setText(
            f"{self.flutter_duration.value() / 10.0:.1f} s"
        )

    def tick(self):
        now = time.monotonic()
        dt = now - self.last
        self.last = now

        # ler sliders
        self.sim.s.tape_friction = self.sl_friction.value() / 100.0
        self.sim.s.encoder_jitter = self.sl_jitter.value() / 100.0
        self.sim.s.encoder_pulse_loss = self.sl_pulse_loss.value() / 100.0
        self.sim.s.encoder_dropout = self.chk_encoder_dropout.isChecked()
        self.sim.s.digital_tach_enabled = self.chk_digital_tach.isChecked()
        self.sim.controller.kp = self.pid_kp.value() / 1_000_000.0
        self.sim.controller.ki = self.pid_ki.value() / 1_000_000.0
        self.sim.controller.kd = self.pid_kd.value() / 1_000_000.0
        disturbances = self.sim.faults.disturbances
        disturbances.wow.set_frequency(self.wow_frequency.value() / 10.0)
        disturbances.wow.set_amplitude(self.wow_amplitude.value() / 10000.0)
        disturbances.wow.set_occurrence(self.wow_occurrence.value() / 100.0)
        disturbances.wow.set_duration(self.wow_duration.value() / 10.0)
        disturbances.flutter.set_frequency(self.flutter_frequency.value() / 10.0)
        disturbances.flutter.set_amplitude(
            self.flutter_amplitude.value() / 10000.0
        )
        disturbances.flutter.set_occurrence(
            self.flutter_occurrence.value() / 100.0
        )
        disturbances.flutter.set_duration(self.flutter_duration.value() / 10.0)

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
            f"Digital Tach: "
            f"{'FALLBACK' if s.control_fallback else ('ON' if s.digital_tach_enabled else 'OFF')} | "
            f"Nominal: {s.command_nominal:+.3f}\n"
            f"P: {s.pid_p:+.3f} | I: {s.pid_i:+.3f} | D: {s.pid_d:+.3f}\n"
            f"Bias: {s.transfer_bias:+.3f} | Req: {s.command_requested:+.3f}\n"
            f"Saturado: {'SIM' if s.actuator_saturated else 'NÃO'} | "
            f"Integral: {'BLOQUEADA' if s.integral_blocked else 'LIVRE'}\n"
            f"RMS: "
            f"{f'{s.rms_error_percent:.3f}%' if s.rms_error_percent is not None else 'estabilizando'}\n"
            f"Atrito: {s.tape_friction:.2f} | Jitter: {s.encoder_jitter:.2f}\n"
            f"Encoder bruto: {s.encoder_rpm_raw:7.1f} RPM\n"
            f"Encoder filtrado: {s.encoder_rpm_filtered:7.1f} RPM | "
            f"Pulsos: {s.encoder_pulse_count}\n"
            f"Perda: {s.encoder_pulse_loss * 100:.0f}% | "
            f"Dropout: {'ON' if s.encoder_dropout else 'OFF'}\n"
            f"Wow: {s.wow_disturbance * 100:+.2f}% | "
            f"Flutter: {s.flutter_disturbance * 100:+.2f}%\n"
            f"Tensão: {s.tension:.3f}"
        )

        # buffers (janela deslizante)
        t = now - self.t0
        self.ts.append(t)
        self.rpm_sp.append(s.rpm_setpoint)
        self.rpm.append(s.rpm)
        self.encoder_rpm.append(s.encoder_rpm_filtered)
        self.encoder_rpm_raw.append(s.encoder_rpm_raw)
        self.pwm.append(s.pwm)
        self.pwm_requested.append(s.command_requested)
        self.err.append(s.err)
        self.tension.append(s.tension)
        if s.rms_error_percent is None:
            self.rms_ts.clear()
            self.rms_percent.clear()
        else:
            self.rms_ts.append(t)
            self.rms_percent.append(s.rms_error_percent)
            while self.rms_ts and (self.rms_ts[-1] - self.rms_ts[0]) > self.window_s:
                self.rms_ts.pop(0)
                self.rms_percent.pop(0)

        # cortar para últimos N segundos
        while self.ts and (self.ts[-1] - self.ts[0]) > self.window_s:
            self.ts.pop(0)
            self.rpm_sp.pop(0)
            self.rpm.pop(0)
            self.encoder_rpm.pop(0)
            self.encoder_rpm_raw.pop(0)
            self.pwm.pop(0)
            self.pwm_requested.pop(0)
            self.err.pop(0)
            self.tension.pop(0)

        # atualizar plots
        self.cur_rpm_sp.setData(self.ts, self.rpm_sp)
        self.cur_rpm.setData(self.ts, self.rpm)
        self.cur_encoder_rpm.setData(self.ts, self.encoder_rpm)
        self.cur_encoder_rpm_raw.setData(self.ts, self.encoder_rpm_raw)
        self.cur_pwm.setData(self.ts, self.pwm)
        self.cur_pwm_requested.setData(self.ts, self.pwm_requested)
        self.cur_err.setData(self.ts, self.err)
        self.cur_tension.setData(self.ts, self.tension)
        self.cur_rms.setData(self.rms_ts, self.rms_percent)


def main():
    app = QApplication(sys.argv)
    interface_font = app.font()
    interface_font.setPointSize(max(interface_font.pointSize() + 4, 13))
    app.setFont(interface_font)
    w = MainWindow()
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
