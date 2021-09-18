#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <QDebug>
#include <QtWidgets>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

const QByteArray get_json_bytes(QString filename) {
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << "Failed to open" << filename;
        exit(1);
    }

    QTextStream text(&file);
    QString json_str = text.readAll();
    file.close();
    const QByteArray bytes = json_str.toLocal8Bit();
    return bytes;
}


QJsonObject get_json_object(const QByteArray bytes) {
    QJsonDocument doc = QJsonDocument::fromJson(bytes);
    if (doc.isNull()) {
        qDebug() << "Failed to create JSON doc";
        exit(2);
    } else if (!doc.isObject()) {
        qDebug() << "JSON is not an object";
        exit(3);
    }

    QJsonObject obj = doc.object();
    if (obj.isEmpty()) {
        qDebug() << "JSON object is empty.";
        exit(4);
    }
    return obj;
}


// "Open" pushbutton. Used to load cached JSON objects from Pycharm project folder.
// NOTE: Code here was adapted from this helpful website by Erick Veil:
// http://erickveil.github.io/2016/04/06/How-To-Manipulate-JSON-With-C++-and-Qt.html

void MainWindow::on_pushButton_clicked()
{
    QString cache_dir = "/Users/logan/PycharmProjects/Weights3/cache";
    QString filename = QFileDialog::getOpenFileName(this, "Open a file", cache_dir);
    const QByteArray json_bytes = get_json_bytes(filename);
    const QJsonObject json_object = get_json_object(json_bytes);

    // access data
    QVariantMap workout = json_object.toVariantMap();
    QVariantList exercises = workout["exercises"].toList();
    for (auto iter1 = exercises.begin(); iter1 != exercises.end(); ++iter1) {
        QVariantMap exercise = iter1->toMap();
        QVariantList sets = exercise["sets"].toList();
        qDebug() << "EXERCISE NAME: " << exercise["name"].toString();
        qDebug() << "Original Line: " << exercise["text"].toString();
        for (auto iter2 = sets.begin(); iter2 != sets.end(); ++iter2) {
            QVariantMap set_ = iter2->toMap();
            qDebug() << "weight is " << set_["weight"].toString();
            qDebug() << "count is " << set_["count"].toString();
            qDebug() << "reps is " << set_["reps"].toString();
        }
    }
}

