# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BrugisDataAccess
                                 A QGIS plugin
 Allow safe and controlled modifications on Brugis Data
                             -------------------
        begin                : 2015-09-24
        copyright            : (C) 2015 by Michel Van Asten GIM
        email                : michelvanasten@gim.be
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
    """Load BrugisDataAccess class from file BrugisDataAccess.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .BdmEditor import BdmEditor
    return BdmEditor(iface)
