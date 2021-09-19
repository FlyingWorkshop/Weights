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
    ui->textEdit->setReadOnly(true);
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

QString extend(QString s1, QString s2) {
    return s1 + s2 + "\n";
}


// creates a single string with line formatting (e.g. to be displayed on a QLabel widget)
QString get_workout_text(const QVariantMap workout) {
    QString result = "";
    QVariantList exercises = workout["exercises"].toList();
    for (auto iter1 = exercises.begin(); iter1 != exercises.end(); ++iter1) {
        QVariantMap exercise = iter1->toMap();
        QVariantList sets = exercise["sets"].toList();
        result = extend(result, "TITLE: " + exercise["name"].toString());
        result = extend(result, "Original: " + exercise["text"].toString());
        for (auto iter2 = sets.begin(); iter2 != sets.end(); ++iter2) {
            QVariantMap set_ = iter2->toMap();
            QString weight = "Weight: " + set_["weight"].toString();
            if (weight != "None") {
                weight = weight + " lbs. ";
            }
            QString count = "Count: " + set_["count"].toString();
            QString reps = "Reps : " + set_["reps"].toString();
            result = extend(result, "\t " + weight + " | " + reps + " | " + count);
          }
    }
    return result;
}


// The "Open" pushbutton is used to load cached JSON objects from Pycharm project folder.
// NOTE: Code here was adapted from this helpful website by Erick Veil:
// http://erickveil.github.io/2016/04/06/How-To-Manipulate-JSON-With-C++-and-Qt.html
void MainWindow::on_pushButton_clicked()
{
    QString cache_dir = "/Users/logan/PycharmProjects/Weights3/cache";
    QString filename = QFileDialog::getOpenFileName(this, "Open a file", cache_dir);
    const QByteArray json_bytes = get_json_bytes(filename);
    const QJsonObject json_object = get_json_object(json_bytes);
    const QVariantMap workout = json_object.toVariantMap();
    QString text = get_workout_text(workout);
    ui->textEdit->append(text);
}


void MainWindow::on_pushButton_2_clicked()
{
    delete ui;
}

