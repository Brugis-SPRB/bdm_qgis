# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BdmAdmin
                                 A QGIS plugin
 BdmAdmin
                             -------------------
        begin                : 2015-10-05
        copyright            : (C) 2015 by Michel Van Asten GIM
        email                : michelvanasten@yahoo.fr
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
    """Load BdmAdmin class from file BdmAdmin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .BdmAdmin import BdmAdmin
    return BdmAdmin(iface)
