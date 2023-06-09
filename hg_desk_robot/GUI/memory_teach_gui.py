# -*- coding:utf8 -*-
#!/usr/bin/python
import glob
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.Qt_UI.memory_teach import Ui_memory_teach
from PyQt5 import QtWidgets, QtCore
from SDK.HG_DR_SDK import HG_DR_SDK

# QtWidgets  QDialog
class memory_window(QtWidgets.QMainWindow, Ui_memory_teach):

    def __init__(self):
        super(memory_window, self).__init__()

        self.setupUi(self)

        path_file_number = glob.glob(pathname='./teach_data/*.txt')  # 获取当前文件夹下个数

        # 记忆示教的记录数
        self.count = 0
        self.hg_dr_sdk = HG_DR_SDK()
        # 气泵默认状态 False-放气 True-吸气
        self.pump_state_now = False
        self.pump_msg = "放气"
        self.lineEdit_8.setText(self.pump_msg)

        self.teach_num = len(path_file_number)  # 示教号

        # 记忆示教位置列表和关节角度
        self.angle_list = []
        self.angle1 = 0.0
        self.angle2 = 0.0
        self.angle3 = 0.0

        # 文本显示列表
        self.item_list = []
    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '记忆示教界面',
                                               "是否要退出记忆示教界面？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:

            if self.angle_list:

                have_data = QtWidgets.QMessageBox.question(self,
                                                       '存在记忆示教数据',
                                                       "是否要保存后再退出？",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)
                if have_data == QtWidgets.QMessageBox.Yes:

                    save_res = self.save_now_teach(True)
                    if save_res == True:
                        self.clear_EditText()
                        event.accept()
                    else:
                        save_fail = QtWidgets.QMessageBox.information(self,
                                                                   '退出保存数据失败',
                                                                   "保存当前示教数据失败, 退出失败, 请重试",
                                                                   QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
                        event.ignore()
                else:
                    self.clear_EditText()
                    event.accept()
        else:
            event.ignore()

    def get_current_angle(self):
        self.angle1, self.angle2, self.angle3, x, y, z = self.hg_dr_sdk.getAngleAndPose()
        information_msg = '获取当前角度成功'
        self.lineEdit.setText(str('%.2f' % self.angle1))
        self.lineEdit_2.setText(str('%.2f' % self.angle2))
        self.lineEdit_3.setText(str('%.2f' % self.angle3))
        QMessageBox.information(self, '获取关节角度', information_msg, QMessageBox.Yes)

    def record_current_angle(self):

        teach_msg = "记录当前关节角度"

        self.itemmodel = QStringListModel(self)

        read_angle1 = self.lineEdit.text()
        read_angle2 = self.lineEdit_2.text()
        read_angle3 = self.lineEdit_3.text()
        if self.pump_state_now:
            pump_data = 1
        else:
            pump_data = 0

        reply = QMessageBox.information(self, '记录关节角度', teach_msg, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.angle_list.append([read_angle1, read_angle2, read_angle3, pump_data])
            # print("记录当前关节角度")
            # print('记录', self.angle_list)
        if self.angle_list:
            # print(self.count)
            self.item_list.append(str(self.angle_list[self.count]) + "," + str(pump_data))
        # print(self.item_list)
        self.itemmodel.setStringList(self.item_list)
        self.listView.setModel(self.itemmodel)
        self.listView.setItemDelegateForColumn(0, EmptyDelegate(self))
        self.count += 1

    def clear_last_operate(self):

        demo_msg = "清除上一个位置"
        reply = QMessageBox.information(self, '返回上一步', demo_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # print("清除上一个位置")
            if self.angle_list:  # 判断 angle_list是否为空
                self.angle_list.pop()
            else:
                no_point_msg = "当前任务已经没有示教点了！"
                QMessageBox.information(self, '无示教点', no_point_msg, QMessageBox.Yes, QMessageBox.Yes)
            if self.count > 0:
                self.item_list.pop()
                self.itemmodel.removeRow(self.count-1)
                self.count -= 1

    def finish_teach(self):

        memory_teach_msg = '结束当前记忆示教任务'
        reply = QMessageBox.information(self, '结束当前记忆示教任务', memory_teach_msg, QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # print("结束当前记忆示教")
            if self.angle_list:
                reply1 = QMessageBox.information(self, '是否保存示教点', "存在已保存的示教点，是否保存", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
                if reply1 == QMessageBox.Yes:
                    self.teach_num += 1
                    f_w = open('./teach_data/teach' + str(self.teach_num) + '.txt', 'w')
                    for i in range(len(self.angle_list)):
                        add_point = '{}, {}, {}, {}\n'.format(self.angle_list[i][0], self.angle_list[i][1],
                                                          self.angle_list[i][2], self.angle_list[i][3])
                        f_w.write(add_point)
                    self.angle_list.clear()
                    f_w.close()
                    save_msg = QMessageBox.question(self, "是否清除", "保存成功，是否清除当前示教任务", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if save_msg == QMessageBox.Yes:
                        self.clear_EditText()
                else:
                    self.clear_EditText()
        # print("结束当前记忆示教任务")

    def start_new_teach(self):
        #判断list是否有数据
        if self.angle_list and self.item_list:
            list_msg = "仍存有示教数据, 请先保存或清理当前数据"
            reply = QMessageBox.information(self, '开始新的记忆示教', list_msg, QMessageBox.Yes)

        # if reply == QMessageBox:
        #     print("开始新的记忆示教")

    def save_now_teach(self, exit_msg=False):

        save_res = False
        memory_teach_msg = '保存当前记忆示教'
        if exit_msg == True:
            memory_teach_msg = "保存当前记忆示教后将直接退出记忆示教"
        reply = QMessageBox.information(self, '保存记忆示教', memory_teach_msg, QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
        if reply == QMessageBox.Yes and self.angle_list:
            self.teach_num += 1
            f_w = open('./teach_data/teach' + str(self.teach_num) + '.txt', 'w')
            for i in range(len(self.angle_list)):
                add_point = '{}, {}, {}, {}\n'.format(self.angle_list[i][0], self.angle_list[i][1],
                                                      self.angle_list[i][2], self.angle_list[i][3])
                f_w.write(add_point)
            # self.angle_list.clear()
            f_w.close()
            save_res = True
            if exit_msg == False:
                clear_msg = "当前记忆示教已保存, 是否清空当前进行的操作？"
                clear_res = QMessageBox.question(self, "保存完毕", clear_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if clear_res == QMessageBox.Yes:
                    self.clear_EditText()
        elif reply == QMessageBox.Yes and len(self.angle_list) == 0:
            no_teach_point = "没有添加任务示教点"
            reply = QMessageBox.information(self, '无示教点', no_teach_point, QMessageBox.Yes,QMessageBox.Yes)
        return save_res

    def pump_up(self):
        self.pump_state_now = True
        self.pump_msg = "吸气"
        self.lineEdit_8.setText(self.pump_msg)

    def pump_down(self):
        self.pump_state_now = False
        self.pump_msg = "放气"
        self.lineEdit_8.setText(self.pump_msg)

    def angle_update(self, angle1, angle2, angle3):
        self.angle1, self.angle2, self.angle3 = angle1, angle2, angle3

    def exit_teach_interface(self):
        self.close()

    def clear_all_operate(self):
        demo_msg = "清除当前任务所有操作"
        reply = QMessageBox.information(self, '清空操作', demo_msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_EditText()

    def clear_EditText(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        if self.count > 0:
            self.itemmodel.removeRows(0, self.count)
        if self.angle_list:
            self.angle_list = []
        if self.item_list:
            self.item_list = []
        self.count = 0

class EmptyDelegate(QItemDelegate):
    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None