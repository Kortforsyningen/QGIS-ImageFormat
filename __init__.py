# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImageFormat
                                 A QGIS plugin
 Image Formatter
                             -------------------
        begin                : 2016-05-10
        copyright            : (C) 2016 by Mafal / sdfe
        email                : mafal@sdfe.dk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ImageFormat class from file ImageFormat.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ImF import ImageFormat
    return ImageFormat(iface)
