

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
    height: 450
    color: "#f3cf1c"
    border.color: "#ffffff"
    focus: true
    activeFocusOnTab: true
    layer.textureMirroring: ShaderEffectSource.MirrorVertically
    z: 0
    layer.enabled: false
    antialiasing: true

    Rectangle {
        id: rectangle2
        x: 100
        y: 5
        width: 300
        height: 50
        color: "#ffffff"
        radius: 7

        BorderImage {
            id: borderImage
            x: 8
            y: 0
            width: 98
            height: 50
            source: "../../../../../../../../Downloads/Untitled-1.png"
            focus: true
            antialiasing: true
            asynchronous: false
            cache: true
            mirror: false
            border.bottom: 5
            border.top: 5
            border.right: 5
            border.left: 5
            horizontalTileMode: BorderImage.Stretch
            clip: false
        }

        BorderImage {
            id: borderImage1
            x: 112
            y: 4
            width: 180
            height: 43
            source: "../../../front_end/logo_diginotas.png"
        }
    }
    Rectangle {
        id: rectangle1
        x: 8
        y: 59
        width: 484
        height: 383
        color: "#ffffff"
        radius: 7

        Column {
            id: column
            x: 8
            y: 8
            width: 468
            height: 322
            rightPadding: 10
            leftPadding: 10
            bottomPadding: 30
            topPadding: 30
            spacing: 20

            Text {
                id: _text
                text: qsTr("Usuário")
                font.letterSpacing: 0.7
                font.pixelSize: 11
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignBottom
                font.capitalization: Font.AllUppercase
                fontSizeMode: Text.FixedSize
                textFormat: Text.StyledText
                font.styleName: "Bold"
                font.family: "Verdana"
            }

            TextField {
                id: textField
                width: 400
                height: 35
                color: "#202121"
                focus: true
                layer.effect: textField
                topInset: 0
                topPadding: 8
                antialiasing: true
                font.preferShaping: false
                font.capitalization: Font.MixedCase
                maximumLength: 100
                selectionColor: "#69621a"
                font.family: "Verdana"
                placeholderTextColor: "#80e8d969"
                transformOrigin: Item.Center
                placeholderText: qsTr("Nome de Login")

                Connections {
                    target: textField
                    onAccepted: textField1.forceActiveFocus()
                }

                Connections {
                    target: textField
                    onAccepted: console.log("test")
                }
            }

            Text {
                id: _text1
                text: qsTr("senha")
                font.letterSpacing: 0.7
                font.pixelSize: 11
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignBottom
                topPadding: 70
                textFormat: Text.StyledText
                fontSizeMode: Text.FixedSize
                font.styleName: "Bold"
                font.family: "Verdana"
                font.capitalization: Font.AllUppercase
            }

            TextField {
                id: textField1
                width: 400
                height: 35
                color: "#202121"
                layer.effect: textField
                echoMode: TextInput.Password
                transformOrigin: Item.Center
                selectionColor: "#69621a"
                placeholderTextColor: "#80e8d969"
                placeholderText: qsTr("Senha")
                maximumLength: 100
                font.preferShaping: false
                font.family: "Verdana"
                font.capitalization: Font.MixedCase
                antialiasing: true

                Connections {
                    target: textField1
                    onAccepted: console.log("test")
                }

                Connections {
                    target: textField1
                    onAccepted: botao_logar.forceActiveFocus()
                }
            }
        }

        Botao_logar {
            id: botao_logar
            x: 8
            y: 340

            Connections {
                target: botao_logar
                onPressed: botao_logar.state = "clicked"
            }

            Connections {
                target: botao_logar
                onClicked: Qt.quit()
            }

            Connections {
                target: botao_logar
                onClicked: botao_logar.state = "Hover"
            }
        }
    }
}
