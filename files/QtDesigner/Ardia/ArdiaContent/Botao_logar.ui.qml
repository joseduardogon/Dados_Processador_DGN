

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import QtQuick.Studio.DesignEffects

Button {
    id: control
    width: 468
    height: 35

    implicitWidth: Math.max(
                       buttonBackground ? buttonBackground.implicitWidth : 0,
                       textItem.implicitWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(
                        buttonBackground ? buttonBackground.implicitHeight : 0,
                        textItem.implicitHeight + topPadding + bottomPadding)
    leftPadding: 4
    rightPadding: 4

    text: "Entrar"

    background: buttonBackground
    Rectangle {
        id: buttonBackground
        color: "#268a20"
        implicitWidth: 100
        implicitHeight: 40
        opacity: enabled ? 1 : 0.3
        radius: 7
        border.color: "#7b268a20"
        layer.enabled: true
        layer.mipmap: true
        layer.smooth: true
        layer.wrapMode: ShaderEffectSource.RepeatVertically
        layer.textureSize.height: 35
        layer.textureSize.width: 468
        layer.effect: buttonBackground
        z: 0
    }

    contentItem: textItem
    Text {
        id: textItem
        x: 0
        width: 468
        font.letterSpacing: 0.7

        opacity: enabled ? 1.0 : 0.3
        color: "#ffffff"
        text: "Entrar"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.capitalization: Font.AllUppercase
        textFormat: Text.AutoText
        font.pointSize: 13
        font.styleName: "Bold"
        font.family: "Verdana"
    }

    states: [
        State {
            name: "Hover"
            when: control.hovered

            PropertyChanges {
                target: buttonBackground
                color: "#195b15"
            }
        },
        State {
            name: "clicked"
            when: control.pressed

            PropertyChanges {
                target: buttonBackground
                color: "#4a268a20"
                border.color: "#268a20"
            }

            PropertyChanges {
                target: textItem
                color: "#2c2c2c"
                text: "Entrar"
            }
        }
    ]
}
