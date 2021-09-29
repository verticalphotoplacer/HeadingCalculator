# -*- coding: utf-8 -*-
"""
/******************************************************************************************
 Heading Calculator
                                 A Standalone Desktop Application
 This tool estimates heading angle for drone photos.
                              -------------------
        begin                : 2020-09-01
        copyright            : (C) 2019-2021 by Chubu University and
               National Research Institute for Earth Science and Disaster Resilience (NIED)
        email                : chuc92man@gmail.com
 ******************************************************************************************/
/******************************************************************************************
 *   This file is part of Heading Calculator.                                             *
 *                                                                                        *
 *   This program is free software; you can redistribute it and/or modify                 *
 *   it under the terms of the GNU General Public License as published by                 *
 *   the Free Software Foundation, version 3 of the License.                              *
 *                                                                                        *
 *   Heading Calculator is distributed in the hope that it will be useful,                *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or    *
 *   FITNESS FOR A PARTICULAR PURPOSE.                                                    *
 *   See the GNU General Public License for more details.                                 *
 *                                                                                        *
 *   You should have received a copy of the GNU General Public License along with         *
 *   Heading Calculator. If not, see <http://www.gnu.org/licenses/>.                      *
 ******************************************************************************************/
"""

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QGraphicsScene, QFrame, QGraphicsItem
from PyQt5.QtGui import QIcon, QBrush, QPen, QColor, QPolygon
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, QDateTime, Qt, QRectF, QPoint
from PyQt5.uic import loadUiType

import traceback, sys
from os.path import join

import resources_rc
import folder_edit
from heading_calculator import headingCalculator
from pyexiftool import resource_path


MAX_THREADS = 2


FORM_CLASS,_ = loadUiType(resource_path('main.ui'))


class QGraphicsArrowItem(QGraphicsItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.x = 0
        self.y = 0
        self.w = 25
        self.h = 0

    def boundingRect(self):
        return QRectF(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget=None):
        painter.save()
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawLine(self.x, self.y, self.w, self.h)
        points = [
            QPoint(17,5),
            QPoint(25,0),
            QPoint(17,-5),
            QPoint(17,5)
            ]

        poly = QPolygon(points)
        painter.drawPolygon(poly)
        painter.restore()


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.func(self.args[0], self.args[1], **self.kwargs)
        except:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Main(QMainWindow, FORM_CLASS):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(join(resource_path('icon'), 'app.png')))
        self.setupUi(self)

        # initialize input variables
        self.folder_name = None
        self.scene = QGraphicsScene()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(MAX_THREADS)
        self.Handel_Buttons()

    def Handel_Buttons(self):

        self.intext.textChanged.connect(self.onIntextChanged)
        self.inbutton.clicked.connect(self.onSelectPhotoFolder)
        self.graphics.setFrameShape(QFrame.NoFrame)
        self.graphics.setScene(self.scene)
        self.button_box.accepted.connect(self.onAccept)
        self.button_box.rejected.connect(self.onClosePlugin)
        self.clearlog.clicked.connect(self.onClearlog)
        self.copylog.clicked.connect(self.onCopylog)
        self.savelog.clicked.connect(self.onSavelog)
        self.clearlog.setIcon(QIcon(join(resource_path('icon'), 'erase.png')))
        self.copylog.setIcon(QIcon(join(resource_path('icon'), 'copypaste.png')))
        self.savelog.setIcon(QIcon(join(resource_path('icon'), 'save2file.png')))

    def onIntextChanged(self):
        """
        Callback for LineEdit change, set content to self.folder_name.

        Returns
        -------
        None.

        """

        self.folder_name = self.intext.text()
        self.progress.setValue(0)

    def onSelectPhotoFolder(self):
        """
        Set content for self.intext when user choose folder via button.

        Returns
        -------
        None.

        """

        folder = QFileDialog.getExistingDirectory(self, "Select folder ")
        # if user do not select any folder, then don't change folder_name
        if len(folder) > 1:
            self.intext.setText(folder)

    def onAccept(self):
        """
        Heading calculator processing.

        Returns
        -------
        None.

        """

        if self.folder_name is not None:
            worker = Worker(headingCalculator, self.folder_name, (".jpg"))
            worker.signals.result.connect(self.writeLog)
            worker.signals.progress.connect(self.onProgressUpdate)
            worker.signals.error.connect(self.error)
            self.threadpool.start(worker)

    def onProgressUpdate(self, n):
        """
        Update processing progress.

        Parameters
        ----------
        n : float
            Percentage of work done.

        Returns
        -------
        None.

        """

        self.progress.setValue(int(n))

    def error(self, e):
        """
        Processing with exception.

        Parameters
        ----------
        e : Exception
            Exception encounted during processing.

        Returns
        -------
        None.

        """

        self.log.appendPlainText("{0}: Task completed!\n {1}\n".format(QDateTime.currentDateTime().toString(Qt.ISODate), e[1]))

    def writeLog(self, result):
        """
        Write results to log widget.

        Parameters
        ----------
        result : string
            Log string.

        Returns
        -------
        None.

        """

        self.display(result["heading"], float(result["avgdist"]))
        self.log.appendPlainText("{0}: Task completed!\n {1}\n".format(QDateTime.currentDateTime().toString(Qt.ISODate), result["msg"]))

    def display(self, files, avgdist):
        """
        Display footprint of photos.

        Parameters
        ----------
        files : 2D list
             Contains photo name, heading, Latitude, Longitude for each photo.

        Returns
        -------
        None.

        """
        multC = 40/avgdist
        try:
            self.scene.clear()

            init_X_GPS, init_Y_GPS = float(files[0][2]), float(files[0][3])
            init_X, init_Y = 0, 0
            for f in files:
                this_X_GPS, this_Y_GPS = float(f[2]), float(f[3])

                pos_X = init_X + multC*(this_X_GPS-init_X_GPS)
                pos_Y = init_Y - multC*(this_Y_GPS-init_Y_GPS)

                rect_item = QGraphicsArrowItem()
                rect_item.setRotation(float(f[1]) - 90)
                rect_item.setPos(pos_X, pos_Y)
                self.scene.addItem(rect_item)

                init_X_GPS, init_Y_GPS = this_X_GPS, this_Y_GPS
                init_X, init_Y = pos_X, pos_Y

            self.scene.setSceneRect(self.scene.itemsBoundingRect())

        except:
            return

    def onClearlog(self):
        """
        Clear log widget.

        Returns
        -------
        None.

        """

        self.log.clear()

    def onCopylog(self):
        """
        Copy log content.

        Returns
        -------
        None.

        """

        self.log.selectAll()
        self.log.copy()

    def onSavelog(self):
        """
        Save log content to a file.

        Returns
        -------
        None.

        """

        try:
            name = QFileDialog.getSaveFileName(self, "Save File", '/', '.txt')[0]
            with open(name, 'w') as f:
                f.write(str(self.log.toPlainText()))
        except:
            return

    def onClosePlugin(self):
        """
        Close the application.

        Returns
        -------
        None.

        """

        self.close()

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()
