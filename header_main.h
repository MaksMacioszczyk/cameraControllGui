#ifndef HEADER_MAIN_H
#define HEADER_MAIN_H

#include <QMainWindow>

namespace Ui {
class main;
}

class main : public QMainWindow
{
    Q_OBJECT

public:
    explicit main(QWidget *parent = nullptr);
    ~main();

private:
    Ui::main *ui;
};

#endif // HEADER_MAIN_H
