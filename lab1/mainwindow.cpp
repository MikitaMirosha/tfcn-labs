#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QList>
#include <QComboBox>
#include <QString>
#include <QTextEdit>
#include <QTime>
#include <QDebug>
#include <QSerialPort>
#include <QSerialPortInfo>

QSerialPort *serial;

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QList<QSerialPortInfo> list;
    list = QSerialPortInfo::availablePorts();

    for(int i = 0; i < list.length(); i++)
        ui->comboBox->addItem(list[i].portName());

    serial = new QSerialPort(this);
    serial->setPortName(ui->comboBox->currentText());
    serial->setBaudRate(QSerialPort::Baud57600);
    serial->setDataBits(QSerialPort::Data8);
    serial->setParity(QSerialPort::NoParity);
    serial->setStopBits(QSerialPort::OneStop);
    serial->setFlowControl(QSerialPort::NoFlowControl);
    serial->open(QIODevice::ReadWrite);
    connect(serial, SIGNAL(readyRead()), this, SLOT(serialReceived()));
    ui->comboBox->hide();

    //---------params---------
    bool boolIsOpen = serial->isOpen();
    const QVariant boolToString(boolIsOpen);
    const QString strIsOpen(boolToString.toString());

    QString strPortName = serial->portName();

    qint32 int32BaudRate = serial->baudRate();
    const QVariant int32ToString(int32BaudRate);
    const QString strBaudRate(int32ToString.toString());

    QSerialPort::Parity spParity = serial->parity();
    const QVariant spParityToInt(spParity);
    const int intParity(spParityToInt.toInt());

    QSerialPort::StopBits spStopBits = serial->stopBits();
    const QVariant spStopBitsToString(spStopBits);
    const QString strStopBits(spStopBitsToString.toString());

    QSerialPort::DataBits spDataBits = serial->dataBits();
    const QVariant spDataBitsToString(spDataBits);
    const QString strDataBits(spDataBitsToString.toString());

    QSerialPort::FlowControl spFlowControl = serial->flowControl();
    //const QVariant spFlowControlToString(spFlowControl);
    const QVariant spFlowControlToInt(spFlowControl);
    const int intFlowControl(spFlowControlToInt.toInt());
    //const QString strFlowControl(spFlowControlToString.toString());

    if(intParity == 0 && intFlowControl == 0)
    {
        const QString strParity = "no";
        const QString strFlowControl = "no";

        ui->textEdit_3->setText(
                                "Ports: "  + strPortName + "->COM2"+ "\n" +
                                "Baud rate: " + strBaudRate + "\n" +
                                "Parity: " + strParity + "\n" +
                                "Stop Bits: " + strStopBits + "\n" +
                                "Data Bits: " + strDataBits + "\n" +
                                "Flow Control: " + strFlowControl + "\n");
    }

    if(intParity == 1 && intFlowControl == 0)
    {
        const QString strParity = "yes";
        const QString strFlowControl = "no";

        ui->textEdit_3->setText(
                                "Ports: "  + strPortName + "->COM2" + "\n" +
                                "Baud rate: " + strBaudRate + "\n" +
                                "Parity: " + strParity + "\n" +
                                "Stop Bits: " + strStopBits + "\n" +
                                "Data Bits: " + strDataBits + "\n" +
                                "Flow Control: " + strFlowControl + "\n");
    }

    if(intParity == 0 && intFlowControl == 1)
    {
        const QString strParity = "no";
        const QString strFlowControl = "yes";

        ui->textEdit_3->setText(
                                "Ports: "  + strPortName + "->COM2" + "\n" +
                                "Baud rate: " + strBaudRate + "\n" +
                                "Parity: " + strParity + "\n" +
                                "Stop Bits: " + strStopBits + "\n" +
                                "Data Bits: " + strDataBits + "\n" +
                                "Flow Control: " + strFlowControl + "\n");
    }

    if(intParity == 1 && intFlowControl == 1)
    {
        const QString strParity = "yes";
        const QString strFlowControl = "yes";

        ui->textEdit_3->setText(
                                "Ports: "  + strPortName + "->COM2" + "\n" +
                                "Baud rate: " + strBaudRate + "\n" +
                                "Parity: " + strParity + "\n" +
                                "Stop Bits: " + strStopBits + "\n" +
                                "Data Bits: " + strDataBits + "\n" +
                                "Flow Control: " + strFlowControl + "\n");
    }
    //---------params---------
}

MainWindow::~MainWindow()
{
    delete ui;
    serial->close();
}

void MainWindow::on_pushButton_2_clicked()
{
    QString sentText = ui->textEdit_2->toPlainText();
    QByteArray inBytes;
    const char *cStrData;
    inBytes = sentText.toUtf8();
    cStrData = inBytes.constData();
    serial->write(cStrData);
    ui->textEdit->setText(sentText);
    ui->textEdit_2->clear();
}

void MainWindow::serialReceived()
{
    QString receivedText = serial->readAll();

    if(receivedText.length() > 0)
        ui->textEdit->setText(receivedText);
}




























