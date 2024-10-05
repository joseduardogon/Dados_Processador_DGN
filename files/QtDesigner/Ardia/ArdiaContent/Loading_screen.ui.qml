

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import Ardia
import QtQuick.Studio.DesignEffects

Rectangle {
    id: rectangle
    width: 500
    height: 100
    color: "#f3cf1c"
    radius: 7
    border.color: "#ffffff"
    focus: true
    activeFocusOnTab: true
    layer.textureMirroring: ShaderEffectSource.MirrorVertically
    z: 0
    layer.enabled: false
    antialiasing: true

    Rectangle {
        id: rectangle1
        x: 150
        y: 8
        width: 200
        height: 33
        color: "#ffffff"
        radius: 7

        Text {
            id: _text
            x: 8
            y: 9
            width: 184
            height: 16
            color: "#2c2c2c"
            text: qsTr("INICIALIZANDO...")
            font.pixelSize: 12
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.styleName: "Bold"
            font.family: "Verdana"
        }
    }

    ProgressBar {
        id: progressBar
        x: 8
        y: 58
        width: 484
        height: 20
        value: 0.5
        focusPolicy: Qt.NoFocus
        enabled: false
        hoverEnabled: false
        indeterminate: true

        Connections {
            target: progressBar
            onValueChanged: Qt.quit()
        }
    }
}
