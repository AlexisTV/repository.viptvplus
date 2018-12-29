################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import zipfile
import uservar
import fnmatch
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin
from resources.libs import extract, downloader, notify, skinSwitch, yt, wizard as wiz

ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID,'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
MYVIDEOS	     = os.path.join(DATABASE,  'MyVideos107.db')
FANART           = os.path.join(ADDONPATH, 'fanart.jpg')
ICON             = os.path.join(ADDONPATH, 'icon.png')
ART              = os.path.join(ADDONPATH, 'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
INSTALLMETHOD    = wiz.getS('installmethod')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFEQ          = wiz.getS('autocleanfeq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
KEEPMYVIDEOS     = wiz.getS('keepmyvideos')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
MYBUILDS         = os.path.join(BACKUPLOCATION, 'MisBuilds', '')
AUTOFEQ          = int(float(AUTOFEQ)) if AUTOFEQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)
KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON 
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
THEME6           = uservar.THEME6
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
MODURL           = 'http://tribeca.tvaddons.ag/tools/maintenance/modules/'
MODURL2          = 'http://mirrors.kodi.tv/addons/jarvis/'
INSTALLMETHODS   = ['Always Ask', 'Reload Profile', 'Force Close']
DEFAULTPLUGINS   = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

def index():
	if AUTOUPDATE == 'Yes':
		if wiz.workingURL(WIZARDFILE) == True:
			ver = wiz.checkWizard('version')
			if ver > VERSION: addFile('%s [v%s] [COLOR red][B][ACTUALIZACION v%s][/B][/COLOR]' % (ADDONTITLE, VERSION, ver), 'wizardupdate', themeit=THEME2)
			else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
		else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	if len(BUILDNAME) > 0:
		version = wiz.checkBuild(BUILDNAME, 'version')
		build = '%s (v%s)' % (BUILDNAME, BUILDVERSION)
		if version > BUILDVERSION: build = '%s [COLOR red][B][ACTUALIZACION v%s][/B][/COLOR]' % (build, version)
		addDir(build,'viewbuild',BUILDNAME, themeit=THEME4)
		themefile = wiz.themeCount(BUILDNAME)
		if not themefile == False:
			addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME5)
	else: addDir('No Instalada', 'builds', themeit=THEME4)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addDir ('Bases y Parches'        ,'builds',   icon=ICONBUILDS,   themeit=THEME1)
	addDir ('Mantenimiento'   ,'maint',    icon=ICONMAINT,    themeit=THEME1)
	if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Instalar Apps Android' ,'apk', icon=ICONAPK, themeit=THEME1)
	if not ADDONFILE == 'http://': addDir ('Instalador de Addons' ,'addons', icon=ICONADDONS, themeit=THEME1)
	if not YOUTUBEFILE == 'http://' and not YOUTUBETITLE == '': addDir (YOUTUBETITLE ,'youtube', icon=ICONYOUTUBE, themeit=THEME1)
	addDir ('Copia de seguridad'     ,'maint', 'backup', icon=ICONSAVE,     themeit=THEME1)
	if HIDECONTACT == 'No': addFile('Contacto' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Ajustes'      ,'settings', icon=ICONSETTINGS, themeit=THEME1)
	if DEVELOPER == 'true': addDir('Developer Menu','developer', icon=ICONSETTINGS, themeit=THEME1)
	setView('files', 'viewType')

def buildMenu():
	WORKINGURL = wiz.workingURL(BUILDFILE)
	if not WORKINGURL == True:
		addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		addDir ('Conservar Data'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:
		total, count15, count16, count17, count18, adultcount, hidden = wiz.buildCount()
		third = False; addin = []
		if THIRDPARTY == 'true':
			if not THIRD1NAME == '' and not THIRD1URL == '': third = True; addin.append('1')
			if not THIRD2NAME == '' and not THIRD2URL == '': third = True; addin.append('2')
			if not THIRD3NAME == '' and not THIRD3URL == '': third = True; addin.append('3')
		link  = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"')
		match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
		if total == 1 and third == False:
			for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				if not DEVELOPER == 'true' and wiz.strTest(name): continue
				viewBuild(match[0][0])
				return
		addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		addDir ('Conservar Data'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		if third == True:
			for item in addin:
				name = eval('THIRD%sNAME' % item)
				addDir ("[B]%s[/B]" % name, 'viewthirdparty', item, icon=ICONBUILDS, themeit=THEME3)
		if len(match) >= 1:
			if SEPERATE == 'true':
				for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if not DEVELOPER == 'true' and wiz.strTest(name): continue
					menu = createMenu('install', '', name)
					addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			else:
				if count17 > 0:
					state = '+' if SHOW17 == 'false' else '-'
					addFile('[B]%s Base y Parches para Kodi 17 Krypton (%s)[/B]' % (state, count17), 'togglesetting',  'show17', themeit=THEME3)
					if SHOW17 == 'false':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 17:
								menu = createMenu('install', '', name)
								addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count18 > 0:
					state = '+' if SHOW18 == 'false' else '-'
					addFile('[B]%s Base y Parches para Kodi 18 Leia (%s)[/B]' % (state, count18), 'togglesetting',  'show18', themeit=THEME3)
					if SHOW18 == 'false':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 18:
								menu = createMenu('install', '', name)
								addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count16 > 0:
					state = '+' if SHOW16 == 'false' else '-'
					addFile('[B]%s Parches extra (%s)[/B]' % (state, count16), 'togglesetting',  'show16', themeit=THEME3)
					if SHOW16 == 'false':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv == 16:
								menu = createMenu('install', '', name)
								addDir('[17/18] %s (v%s)' % (name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count15 > 0:
					state = '+' if SHOW15 == 'false' else '-'
					addFile('[B]%s Versiones anteriores (%s)[/B]' % (state, count15), 'togglesetting',  'show15', themeit=THEME3)
					if SHOW15 == 'false':
						for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
							if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
							if not DEVELOPER == 'true' and wiz.strTest(name): continue
							kodiv = int(float(kodi))
							if kodiv <= 15:
								menu = createMenu('install', '', name)
								addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
		elif hidden > 0: 
			if adultcount > 0:
				addFile('There is currently only Adult builds', '', icon=ICONBUILDS, themeit=THEME3)
				addFile('Enable Show Adults in Addon Settings > Misc', '', icon=ICONBUILDS, themeit=THEME3)
			else:
				addFile('Currently No Builds Offered from %s' % ADDONTITLE, '', icon=ICONBUILDS, themeit=THEME3)
		else: addFile('Text file for builds not formated correctly.', '', icon=ICONBUILDS, themeit=THEME3)
	setView('files', 'viewType')

def viewBuild(name):
	WORKINGURL = wiz.workingURL(BUILDFILE)
	if not WORKINGURL == True:
		addFile('Url for txt file not valid', '', themeit=THEME3)
		addFile('%s' % WORKINGURL, '', themeit=THEME3)
		return
	if wiz.checkBuild(name, 'version') == False: 
		addFile('Error reading the txt file.', '', themeit=THEME3)
		addFile('%s was not found in the builds list.' % name, '', themeit=THEME3)
		return
	link = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % name).findall(link)
	for version, url, gui, kodi, themefile, icon, fanart, preview, adult, description in match:
		icon        = icon   if wiz.workingURL(icon)   else ICON
		fanart      = fanart if wiz.workingURL(fanart) else FANART
		build       = '%s (v%s)' % (name, version)
		if BUILDNAME == name and version > BUILDVERSION:
			build = '%s [COLOR red][Ultima v%s][/COLOR]' % (build, BUILDVERSION)
		addFile(build, '', description=description, fanart=fanart, icon=icon, themeit=THEME6)
		if HIDESPACERS == 'No': addFile(wiz.sep('INFO'), '', themeit=THEME3)
		addFile('Ver cambios y notas',    'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		if not preview == "http://": addFile('Ver Video Presentacion', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		addDir ('Guardar Addon_data',    'backupaddon', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		addDir ('Conservar Data',       'savedata', icon=ICONSAVE,     themeit=THEME3)
		temp1 = int(float(KODIV)); temp2 = int(float(kodi))
		if not temp1 == temp2: 
			if temp1 == 16 and temp2 <= 15: warning = False
			else: warning = True
		else: warning = False
		if warning == True:
			addFile('(%s) [I]Comprueba que esta Base/Parche es para tu version de Kodi: %s)[/I]' % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile(wiz.sep('INSTALACION'), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile('[COLOR lime][B][VERSION BASE][/B][/COLOR] Pulsa aqui para instalar una Build'   , 'install', name, 'fresh'  , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		addFile('[COLOR yellow][B][PARCHES][/B][/COLOR] Pulsa aqui para instalar un Parche', 'install', name, 'normal' , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not gui == 'http://': addFile('Instalar Ajustes de Kodi'    , 'install', name, 'gui'     , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not themefile == 'http://':
			if wiz.workingURL(themefile) == True:
				addFile(wiz.sep('THEMES'), '', fanart=fanart, icon=icon, themeit=THEME3)
				link  = wiz.openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
				for themename, themeurl, themeicon, themefanart, themeadult, description in match:
					if not SHOWADULT == 'true' and themeadult.lower() == 'yes': continue
					themeicon   = themeicon   if themeicon   == 'http://' else icon
					themefanart = themefanart if themefanart == 'http://' else fanart
					addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=THEME3)
	setView('files', 'viewType')

def viewThirdList(number):
	name = eval('THIRD%sNAME' % number)
	url  = eval('THIRD%sURL' % number)
	work = wiz.workingURL(url)
	if not work == True:
		addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:
		type, buildslist = wiz.thirdParty(url)
		addFile("[B]%s[/B]" % name, '', themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		if type:
			for name, version, url, kodi, icon, fanart, adult, description in buildslist:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				addFile("[%s] %s v%s" % (kodi, name, version), 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)
		else:
			for name, url, icon, fanart, description in buildslist:
				addFile(name, 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)

def editThirdParty(number):
	name  = eval('THIRD%sNAME' % number)
	url   = eval('THIRD%sURL' % number)
	name2 = wiz.getKeyboard(name, 'Introduce el nombre de la build/wizard')
	url2  = wiz.getKeyboard(url, 'Introduce la URL del archivo wizard de la Build')
	
	wiz.setS('wizard%sname' % number, name2)
	wiz.setS('wizard%surl' % number, url2)

def apkScraper(name=""):
	if name == 'kodi':
		kodiurl1 = 'http://mirrors.kodi.tv/releases/android/arm/'
		url1 = wiz.openURL(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
		x = 0
		match1 = re.compile('<tr><td><a href="(.+?)">(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
		
		addFile("Versiones oficiales Kodi", themeit=THEME1)
		rc = False
		for url, name, size, date in match1:
			if not url.endswith('.apk'): continue
			if not url.find('_') == -1 and rc == True: continue
			try:
				tempname = name.split('-')
				if not url.find('_') == -1:
					rc = True
					name2, v2 = tempname[2].split('_')
				else: 
					name2 = tempname[2]
					v2 = ''
				title = "[COLOR %s]%s v%s%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, COLOR2, size.replace(' ', ''), COLOR1, date)
				download = urljoin(kodiurl1, url)
				addFile(title, 'apkinstall', "%s v%s%s %s" % (tempname[0].title(), tempname[1], v2.upper(), name2), download)
				x += 1
			except:
				wiz.log("Error on: %s" % name)
		if x == 0: addFile("Error Kodi Scraper Is Currently Down.")
	

def apkMenu(url=None):
	if url == None:
		addDir ('Versiones Kodi', 'apkscrape', 'kodi', icon=ICONAPK, themeit=THEME1)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	if not APKFILE == 'http://':
		if url == None:
			APKWORKING  = wiz.workingURL(APKFILE)
			TEMPAPKFILE = uservar.APKFILE
		else:
			APKWORKING  = wiz.workingURL(url)
			TEMPAPKFILE = url
		if APKWORKING == True:
			link = wiz.openURL(TEMPAPKFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for name, section, url, icon, fanart, adult, description in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if section.lower() == 'yes':
						x += 1
						addDir ("[B]%s[/B]" % name, 'apk', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						x += 1
						addFile(name, 'apkinstall', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					if x < 1:
						addFile("No addons added to this menu yet!", '', themeit=THEME2)
			else: wiz.log("[APK Menu] ERROR: Invalid Format.", xbmc.LOGERROR)
		else: 
			wiz.log("[APK Menu] ERROR: URL for apk list not working.", xbmc.LOGERROR)
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % APKWORKING, '', themeit=THEME3)
		return
	else: wiz.log("[APK Menu] No APK list added.")
	setView('files', 'viewType')

def addonMenu(url=None):
	if not ADDONFILE == 'http://':
		if url == None:
			ADDONWORKING  = wiz.workingURL(ADDONFILE)
			TEMPADDONFILE = uservar.ADDONFILE
		else:
			ADDONWORKING  = wiz.workingURL(url)
			TEMPADDONFILE = url
		if ADDONWORKING == True:
			link = wiz.openURL(TEMPADDONFILE).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for name, plugin, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if plugin.lower() == 'section':
						x += 1
						addDir ("[B]%s[/B]" % name, 'addons', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						try:
							add    = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
							if os.path.exists(add):
								name   = "[COLOR green][Installed][/COLOR] %s" % name
						except:
							pass
						x += 1
						addFile(name, 'addoninstall', plugin, TEMPADDONFILE, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					if x < 1:
						addFile("No addons added to this menu yet!", '', themeit=THEME2)
			else: 
				addFile('Text File not formated correctly!', '', themeit=THEME3)
				wiz.log("[Addon Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[Addon Menu] ERROR: URL for Addon list not working.")
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % ADDONWORKING, '', themeit=THEME3)
	else: wiz.log("[Addon Menu] No Addon list added.")
	setView('files', 'viewType')

def addonInstaller(plugin, url):
	if not ADDONFILE == 'http://':
		ADDONWORKING = wiz.workingURL(url)
		if ADDONWORKING == True:
			link = wiz.openURL(url).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
			if len(match) > 0:
				for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if os.path.exists(os.path.join(ADDONS, plugin)):
						do        = ['Launch Addon', 'Remove Addon']
						selected = DIALOG.select("[COLOR %s]Addon already installed what would you like to do?[/COLOR]" % COLOR2, do)
						if selected == 0:
							wiz.ebi('RunAddon(%s)' % plugin)
							xbmc.sleep(500)
							return True
						elif selected == 1:
							wiz.cleanHouse(os.path.join(ADDONS, plugin))
							try: wiz.removeFolder(os.path.join(ADDONS, plugin))
							except: pass
							if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to remove the addon_data for:" % COLOR2, "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR green]Yes Remove[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
								removeAddonData(plugin)
							wiz.refresh()
							return True
						else:
							return False
					repo = os.path.join(ADDONS, repository)
					if not repository.lower() == 'none' and not os.path.exists(repo):
						wiz.log("Repository not installed, installing it")
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to install the repository for [COLOR %s]%s[/COLOR]:" % (COLOR2, COLOR1, plugin), "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, repository), yeslabel="[B][COLOR green]Yes Install[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): 
							ver = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': repository})
							if len(ver) > 0:
								repozip = '%s%s-%s.zip' % (repositoryurl, repository, ver[0])
								wiz.log(repozip)
								if KODIV >= 17: wiz.addonDatabase(repository, 1)
								installAddon(repository, repozip)
								wiz.ebi('UpdateAddonRepos()')
								#wiz.ebi('UpdateLocalAddons()')
								wiz.log("Installing Addon from Kodi")
								install = installFromKodi(plugin)
								wiz.log("Install from Kodi: %s" % install)
								if install:
									wiz.refresh()
									return True
							else:
								wiz.log("[Addon Installer] Repository not installed: Unable to grab url! (%s)" % repository)
						else: wiz.log("[Addon Installer] Repository for %s not installed: %s" % (plugin, repository))
					elif repository.lower() == 'none':
						wiz.log("No repository, installing addon")
						pluginid = plugin
						zipurl = url
						installAddon(plugin, url)
						wiz.refresh()
						return True
					else:
						wiz.log("Repository installed, installing addon")
						install = installFromKodi(plugin, False)
						if install:
							wiz.refresh()
							return True
					if os.path.exists(os.path.join(ADDONS, plugin)): return True
					ver2 = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': plugin})
					if len(ver2) > 0:
						url = "%s%s-%s.zip" % (url, plugin, ver2[0])
						wiz.log(str(url))
						if KODIV >= 17: wiz.addonDatabase(plugin, 1)
						installAddon(plugin, url)
						wiz.refresh()
					else: 
						wiz.log("no match"); return False
			else: wiz.log("[Addon Installer] Invalid Format")
		else: wiz.log("[Addon Installer] Text File: %s" % ADDONWORKING)
	else: wiz.log("[Addon Installer] Not Enabled.")

def installFromKodi(plugin, over=True):
	if over == True:
		xbmc.sleep(2000)
	#wiz.ebi('InstallAddon(%s)' % plugin)
	wiz.ebi('RunPlugin(plugin://%s)' % plugin)
	if not wiz.whileWindow('yesnodialog'):
		return False
	xbmc.sleep(500)
	if wiz.whileWindow('okdialog'):
		return False
	wiz.whileWindow('progressdialog')
	if os.path.exists(os.path.join(ADDONS, plugin)): return True
	else: return False

def installAddon(name, url):
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
	urlsplit = url.split('/')
	lib=os.path.join(PACKAGES, urlsplit[-1])
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
	DP.update(0, title,'', '[COLOR %s]Installing Dependencies[/COLOR]' % COLOR2)
	installed(name)
	installDep(name, DP)
	DP.close()
	wiz.ebi('UpdateAddonRepos()')
	wiz.ebi('UpdateLocalAddons()')
	wiz.refresh()

def installDep(name, DP=None):
	dep=os.path.join(ADDONS,name,'addon.xml')
	if os.path.exists(dep):
		source = open(dep,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		for depends in match:
			if not 'xbmc.python' in depends:
				if not DP == None:
					DP.update(0, '', '[COLOR %s]%s[/COLOR]' % (COLOR1, depends))
				wiz.createTemp(depends)
				# continue
				# dependspath=os.path.join(ADDONS, depends)
				# if not os.path.exists(dependspath):
					# zipname = '%s-%s.zip' % (depends, match2[match.index(depends)])
					# depzip = urljoin("%s%s/" % (MODURL2, depends), zipname)
					# if not wiz.workingURL(depzip) == True:
						# depzip = urljoin(MODURL, '%s.zip' % depends)
						# if not wiz.workingURL(depzip) == True:
							# wiz.createTemp(depends)
							# if KODIV >= 17: wiz.addonDatabase(depends, 1)
							# continue
					# lib=os.path.join(PACKAGES, '%s.zip' % depends)
					# try: os.remove(lib)
					# except: pass
					# DP.update(0, '[COLOR %s][B]Downloading Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends),'', 'Please Wait')
					# downloader.download(depzip, lib, DP)
					# xbmc.sleep(100)
					# title = '[COLOR %s][B]Installing Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends)
					# DP.update(0, title,'', 'Please Wait')
					# percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
					# if KODIV >= 17: wiz.addonDatabase(depends, 1)
					# installed(depends)
					# installDep(depends)
					# xbmc.sleep(100)
					# DP.close()

def installed(addon):
	url = os.path.join(ADDONS,addon,'addon.xml')
	if os.path.exists(url):
		try:
			list  = open(url,mode='r'); g = list.read(); list.close()
			name = wiz.parseDOM(g, 'addon', ret='name', attrs = {'id': addon})
			icon  = os.path.join(ADDONS,addon,'icon.png')
			wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, name[0]), '[COLOR %s]Addon Enabled[/COLOR]' % COLOR2, '2000', icon)
		except: pass

def youtubeMenu(url=None):
	if not YOUTUBEFILE == 'http://':
		if url == None:
			YOUTUBEWORKING  = wiz.workingURL(YOUTUBEFILE)
			TEMPYOUTUBEFILE = uservar.YOUTUBEFILE
		else:
			YOUTUBEWORKING  = wiz.workingURL(url)
			TEMPYOUTUBEFILE = url
		if YOUTUBEWORKING == True:
			link = wiz.openURL(TEMPYOUTUBEFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, section, url, icon, fanart, description in match:
					if section.lower() == "yes":
						addDir ("[B]%s[/B]" % name, 'youtube', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						addFile(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[YouTube Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % YOUTUBEWORKING, '', themeit=THEME3)
	else: wiz.log("[YouTube Menu] No YouTube list added.")
	setView('files', 'viewType')

def maintMenu(view=None):
	on = '[B][COLOR green]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
	autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
	cache       = 'true' if AUTOCACHE      == 'true' else 'false'
	packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
	thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
	maint       = 'true' if SHOWMAINT      == 'true' else 'false'
	thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
	if wiz.Grab_Log(True) == False: kodilog = 0
	else: kodilog = errorChecking(wiz.Grab_Log(True), True, True)
	if wiz.Grab_Log(True, True) == False: kodioldlog = 0
	else: kodioldlog = errorChecking(wiz.Grab_Log(True,True), True, True)
	errorsinlog = int(kodilog) + int(kodioldlog)
	errorsfound = str(errorsinlog) + ' Error(es) Encontrados' if errorsinlog > 0 else 'No hay'
	wizlogsize = ': [COLOR red]No hay[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR green]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
	sizepack   = wiz.getSize(PACKAGES)
	sizethumb  = wiz.getSize(THUMBS)
	sizecache  = wiz.getCacheSize()
	feq        = ['Always', 'Daily', '3 Days', 'Weekly']
	addDir ('[B]Herramientas de Limpieza[/B]'       ,'maint', 'clean',  icon=ICONMAINT, themeit=THEME1)
	if view == "clean" or SHOWMAINT == 'true': 
		addFile('Limpiar Thumbnails antiguos', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
		addFile('Limpiar Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)
		addFile('Limpiar Database',                'purgedb',         icon=ICONMAINT, themeit=THEME3)
		addFile('Fresh Start (Limpieza Total)',                    'freshstart',      icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Configurar Auto Limpieza[/B]'     ,'maint', 'autoclean',   icon=ICONMAINT, themeit=THEME1)
	if view == "autoclean" or SHOWMAINT == 'true':
		addFile('Auto Limpieza al iniciar Kodi: %s' % autoclean.replace('true',on).replace('false',off) ,'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME3)
		addFile('--- Frecuencia de la Auto Limpieza: [B][COLOR green]%s[/COLOR][/B]' % feq[AUTOFEQ], 'changefeq', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Limpiar Cache al inicio: %s' % cache.replace('true',on).replace('false',off), 'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Limpiar paquetes al inicio: %s' % packages.replace('true',on).replace('false',off), 'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Limpiar miniaturas al inicio: %s' % thumbs.replace('true',on).replace('false',off), 'togglesetting', 'clearthumbs', icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Herramientas para Addons[/B]',       'maint', 'addon',  icon=ICONMAINT, themeit=THEME1)
	if view == "addon" or SHOWMAINT == 'true': 
		addFile('Desinstalar Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
		addDir ('Borrar Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
		addDir ('Activar/Desactivar Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
		addFile('Activar/Desactivar Addons para Adultos',    'toggleadult',     icon=ICONMAINT, themeit=THEME3)
		addFile('Forzar Actualizacion de Addons',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Herramientas de Mantenimiento[/B]'     ,'maint', 'misc',   icon=ICONMAINT, themeit=THEME1)
	if view == "misc" or SHOWMAINT == 'true': 
		addFile('Recargar Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
		addFile('Recargar Perfil',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)
		addFile('Forzar Cierre de Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)
		addFile('Escanear fuentes de contenido por links rotos',  'checksources',    icon=ICONMAINT, themeit=THEME3)
		addFile('Escanear Repositorios rotos',   'checkrepos',      icon=ICONMAINT, themeit=THEME3)
		addFile('Ver errores en Log: %s' % (errorsfound), 'viewerrorlog',    icon=ICONMAINT, themeit=THEME3)
		addFile('Ver Log',                  'viewlog',         icon=ICONMAINT, themeit=THEME3)
		addFile('Ver Wizard Log',           'viewwizlog',      icon=ICONMAINT, themeit=THEME3)
		addFile('Limpiar Wizard Log%s' % wizlogsize,'clearwizlog',     icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Copia de Seguridad / Restauracion[/B]'     ,'maint', 'backup',   icon=ICONMAINT, themeit=THEME1)
	if view == "backup" or SHOWMAINT == 'true':
		addFile('Limpiar carpeta de copias de seguridad',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
		addFile('Ubicacion de la copia de seguridad: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
		addFile('[Guardar]: Build Completa',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Guardar]: Skin y Menus',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Guardar]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restaurar]: Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restaurar]: Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restaurar]: Skin y Menus',     'restoretheme',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restaurar]: Build Externa',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restaurar]: Addon_data Externo', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
	addDir ('[B]Advanced Settings[/B]',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
	if view == "tweaks" or SHOWMAINT == 'true': 
		if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
			addDir ('Instalar Buffer (Advanced Settings)',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
		else: 
			if os.path.exists(ADVANCED):
				addFile('Ver actual AdvancedSettings.xml',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
				addFile('Borrar actual AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
			addFile('Hacer Configuracion personalizada de AdvancedSettings.xml',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)
	addFile('Agrega tu Wizard: %s' % thirdparty.replace('true',on).replace('false',off) ,'togglesetting', 'enable3rd', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
	if thirdparty == 'true':
		first = THIRD1NAME if not THIRD1NAME == '' else 'No agregado'
		secon = THIRD2NAME if not THIRD2NAME == '' else 'No agregado'
		third = THIRD3NAME if not THIRD3NAME == '' else 'No agregado'
		addFile('Editar Wizard 1: [COLOR %s]%s[/COLOR]' % (COLOR2, first), 'editthird', '1', icon=ICONMAINT, themeit=THEME3)
		addFile('Editar Wizard 2: [COLOR %s]%s[/COLOR]' % (COLOR2, secon), 'editthird', '2', icon=ICONMAINT, themeit=THEME3)
		addFile('Editar Wizard 3: [COLOR %s]%s[/COLOR]' % (COLOR2, third), 'editthird', '3', icon=ICONMAINT, themeit=THEME3)
	setView('files', 'viewType')
	addFile('Abrir todos los menus de Mantenimiento: %s' % maint.replace('true',on).replace('false',off) ,'togglesetting', 'showmaint', icon=ICONMAINT, themeit=THEME2)
	addDir ('[I]<< Volver al Menu Principal[/I]', icon=ICONMAINT, themeit=THEME2)



def advancedWindow(url=None):
	if not ADVANCEDFILE == 'http://':
		if url == None:
			ADVANCEDWORKING = wiz.workingURL(ADVANCEDFILE)
			TEMPADVANCEDFILE = uservar.ADVANCEDFILE
		else:
			ADVANCEDWORKING  = wiz.workingURL(url)
			TEMPADVANCEDFILE = url
		addFile('Click para Configuracion personalizada del AdvancedSettings.xml', 'autoadvanced', icon=ICONMAINT, themeit=THEME3)
		addFile('Forzar Cierre de Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)

		if os.path.exists(ADVANCED): 
			addFile('Ver el actual AdvancedSettings.xml', 'currentsettings', icon=ICONMAINT, themeit=THEME3)
			addFile('Borrar AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
		if ADVANCEDWORKING == True:
			if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONMAINT, themeit=THEME3)
			link = wiz.openURL(TEMPADVANCEDFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, section, url, icon, fanart, description in match:
					if section.lower() == "yes":
						addDir ("[B]%s[/B]" % name, 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						addFile(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[Advanced Settings] ERROR: Invalid Format.")
		else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
	else: wiz.log("[Advanced Settings] not Enabled")

def writeAdvanced(name, url):
	ADVANCEDWORKING = wiz.workingURL(url)
	if ADVANCEDWORKING == True:
		if os.path.exists(ADVANCED): choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres sobreescribir el actual Advanced Settings con el archivo [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR green]Sobreescribir[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")
		else: choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres descargar e instalar [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR green]Instalar[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")

		if choice == 1:
			file = wiz.openURL(url)
			f = open(ADVANCED, 'w'); 
			f.write(file)
			f.close()
			DIALOG.ok(ADDONTITLE, '[COLOR %s]AdvancedSettings.xml se ha creado/escrito con exito.  Una vez que hagas click en aceptar se forzara el cierre de Kodi.[/COLOR]' % COLOR2)
			wiz.killxbmc(True)
		else: wiz.log("[Advanced Settings] install canceled"); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]Escritura cancelada![/COLOR]" % COLOR2); return
	else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]URL No Funciona[/COLOR]" % COLOR2)

def viewAdvanced():
	f = open(ADVANCED)
	a = f.read().replace('\t', '    ')
	wiz.TextBox(ADDONTITLE, a)
	f.close()

def removeAdvanced():
	if os.path.exists(ADVANCED):
		wiz.removeFile(ADVANCED)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml no encontrado[/COLOR]")

def showAutoAdvanced():
	notify.autoConfig()

def getIP():
	site  = 'http://whatismyipaddress.com/'
	if not wiz.workingURL(site): return 'Unknown', 'Unknown', 'Unknown'
	page  = wiz.openURL(site).replace('\n','').replace('\r','')
	if not 'Access Denied' in page:
		ipmatch   = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(page)
		ipfinal   = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
		details   = re.compile('"font-size:14px;">(.+?)</td>').findall(page)
		provider  = details[0] if (len(details) > 0) else 'Unknown'
		location  = details[1]+', '+details[2]+', '+details[3] if (len(details) > 2) else 'Unknown'
		return ipfinal, provider, location
	else: return 'Unknown', 'Unknown', 'Unknown'

def systemInfo():
	infoLabel = ['System.FriendlyName', 
				 'System.BuildVersion', 
				 'System.CpuUsage',
				 'System.ScreenMode',
				 'Network.IPAddress',
				 'Network.MacAddress',
				 'System.Uptime',
				 'System.TotalUptime',
				 'System.FreeSpace',
				 'System.UsedSpace',
				 'System.TotalSpace',
				 'System.Memory(free)',
				 'System.Memory(used)',
				 'System.Memory(total)']
	data      = []; x = 0
	for info in infoLabel:
		temp = wiz.getInfo(info)
		y = 0
		while temp == "Busy" and y < 10:
			temp = wiz.getInfo(info); y += 1; wiz.log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
		data.append(temp)
		x += 1
	storage_free  = data[8] if 'Una' in data[8] else wiz.convertSize(int(float(data[8][:-8]))*1024*1024)
	storage_used  = data[9] if 'Una' in data[9] else wiz.convertSize(int(float(data[9][:-8]))*1024*1024)
	storage_total = data[10] if 'Una' in data[10] else wiz.convertSize(int(float(data[10][:-8]))*1024*1024)
	ram_free      = wiz.convertSize(int(float(data[11][:-2]))*1024*1024)
	ram_used      = wiz.convertSize(int(float(data[12][:-2]))*1024*1024)
	ram_total     = wiz.convertSize(int(float(data[13][:-2]))*1024*1024)
	exter_ip, provider, location = getIP()
	
	picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []
	
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername == 'packages': continue
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			prov   = re.compile("<provides>(.+?)</provides>").findall(a)
			if len(prov) == 0:
				if foldername.startswith('skin'): skins.append(foldername)
				if foldername.startswith('repo'): repos.append(foldername)
				else: scripts.append(foldername)
			elif not (prov[0]).find('executable') == -1: programs.append(foldername)
			elif not (prov[0]).find('video') == -1: video.append(foldername)
			elif not (prov[0]).find('audio') == -1: music.append(foldername)
			elif not (prov[0]).find('image') == -1: picture.append(foldername)

	addFile('[B]Media Center Info:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Name:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[0]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Version:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[1]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Platform:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, wiz.platform().title()), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]CPU Usage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[2]), '', icon=ICONMAINT, themeit=THEME3)
	addFile('[COLOR %s]Screen Mode:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[3]), '', icon=ICONMAINT, themeit=THEME3)
	
	addFile('[B]Uptime:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Current Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[6]), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[7]), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]Local Storage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Used Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_free), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Free Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_used), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_total), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]Ram Usage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Used Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_free), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Free Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_used), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Total Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_total), '', icon=ICONMAINT, themeit=THEME2)
	
	addFile('[B]Network:[/B]', '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Local IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[4]), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, exter_ip), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Provider:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, provider), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Location:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, location), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]MacAddress:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[5]), '', icon=ICONMAINT, themeit=THEME2)
	
	totalcount = len(picture) + len(music) + len(video) + len(programs) + len(scripts) + len(skins) + len(repos) 
	addFile('[B]Addons([COLOR %s]%s[/COLOR]):[/B]' % (COLOR1, totalcount), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Video Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(video))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Program Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(programs))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Music Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(music))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Picture Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(picture))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(repos))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Skins:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(skins))), '', icon=ICONMAINT, themeit=THEME2)
	addFile('[COLOR %s]Scripts/Modules:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(scripts))), '', icon=ICONMAINT, themeit=THEME2)	
	
def saveMenu():
	on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
	myvideos   = 'true' if KEEPMYVIDEOS  == 'true' else 'false'
	sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
	advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
	profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
	favourites = 'true' if KEEPFAVS      == 'true' else 'false'
	repos      = 'true' if KEEPREPOS     == 'true' else 'false'
	super      = 'true' if KEEPSUPER     == 'true' else 'false'
	whitelist  = 'true' if KEEPWHITELIST == 'true' else 'false'

	addFile('Importar Save Data',              'managedata', 'import', icon=ICONSAVE,  themeit=THEME1)
	addFile('Exportar Save Data',              'managedata', 'export', icon=ICONSAVE,  themeit=THEME1)
	addFile('- Click para cambiar ajustes -', '', themeit=THEME3)
	addFile('Mantener Videoteca \'MyVideos107.db\': %s' % myvideos.replace('true',on).replace('false',off)           ,'togglesetting', 'keepmyvideos',    icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener fuentes de contenido \'Sources.xml\': %s' % sources.replace('true',on).replace('false',off)           ,'togglesetting', 'keepsources',    icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener Info Perfiles \'Profiles.xml\': %s' % profiles.replace('true',on).replace('false',off)         ,'togglesetting', 'keepprofiles',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener Buffer \'Advancedsettings.xml\': %s' % advanced.replace('true',on).replace('false',off) ,'togglesetting', 'keepadvanced',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener \'Favourites.xml\': %s' % favourites.replace('true',on).replace('false',off)     ,'togglesetting', 'keepfavourites', icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener Super Favourites: %s' % super.replace('true',on).replace('false',off)            ,'togglesetting', 'keepsuper',      icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener Repos instaladas\'s: %s' % repos.replace('true',on).replace('false',off)           ,'togglesetting', 'keeprepos',      icon=ICONSAVE,  themeit=THEME1)
	addFile('Mantener Mi \'WhiteList\': %s' % whitelist.replace('true',on).replace('false',off)        ,'togglesetting', 'keepwhitelist',  icon=ICONSAVE,  themeit=THEME1)
	if whitelist == 'true':
		addFile('Edit My Whitelist',        'whitelist', 'edit',   icon=ICONSAVE,  themeit=THEME1)
		addFile('View My Whitelist',        'whitelist', 'view',   icon=ICONSAVE,  themeit=THEME1)
		addFile('Clear My Whitelist',       'whitelist', 'clear',  icon=ICONSAVE,  themeit=THEME1)
		addFile('Import My Whitelist',      'whitelist', 'import', icon=ICONSAVE,  themeit=THEME1)
		addFile('Export My Whitelist',      'whitelist', 'export', icon=ICONSAVE,  themeit=THEME1)
	setView('files', 'viewType')


def fixUpdate():
	if KODIV < 17: 
		dbfile = os.path.join(DATABASE, wiz.latestDB('Addons'))
		try:
			os.remove(dbfile)
		except Exception, e:
			wiz.log("Unable to remove %s, Purging DB" % dbfile)
			wiz.purgeDb(dbfile)
	else:
		xbmc.log("Requested Addons.db be removed but doesnt work in Kod17")

def removeAddonMenu():
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	addonnames = []; addonids = []
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		elif foldername in DEFAULTPLUGINS: continue
		elif foldername == 'packages': continue
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			match  = wiz.parseDOM(a, 'addon', ret='id')

			addid  = foldername if len(match) == 0 else match[0]
			try: 
				add = xbmcaddon.Addon(id=addid)
				addonnames.append(add.getAddonInfo('name'))
				addonids.append(addid)
			except:
				pass
	if len(addonnames) == 0:
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Addons To Remove[/COLOR]" % COLOR2)
		return
	if KODIV > 16:
		selected = DIALOG.multiselect("%s: Elige los addons que quieres borrar." % ADDONTITLE, addonnames)
	else:
		selected = []; choice = 0
		tempaddonnames = ["-- Click here to Continue --"] + addonnames
		while not choice == -1:
			choice = DIALOG.select("%s: Select the addons you wish to remove." % ADDONTITLE, tempaddonnames)
			if choice == -1: break
			elif choice == 0: break
			else: 
				choice2 = (choice-1)
				if choice2 in selected:
					selected.remove(choice2)
					tempaddonnames[choice] = addonnames[choice2]
				else:
					selected.append(choice2)
					tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
	if selected == None: return
	if len(selected) > 0:
		wiz.addonUpdates('set')
		for addon in selected:
			removeAddon(addonids[addon], addonnames[addon], True)

		xbmc.sleep(500)
		
		if INSTALLMETHOD == 1: todo = 1
		elif INSTALLMETHOD == 2: todo = 0
		else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR green]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
		if todo == 1: wiz.reloadFix('remove addon')
		else: wiz.addonUpdates('reset'); wiz.killxbmc(True)

def removeAddonDataMenu():
	if os.path.exists(ADDOND):
		addFile('[COLOR red][B][BORRAR][/B][/COLOR] Todas las carpetas de Addon_Data', 'removedata', 'all', themeit=THEME2)
		addFile('[COLOR red][B][BORRAR][/B][/COLOR] Todas las carpetas Addon_data de Addons desinstalados', 'removedata', 'uninstalled', themeit=THEME2)
		addFile('[COLOR red][B][BORRAR][/B][/COLOR] Todas las carpetas vacias de Addon_Data', 'removedata', 'empty', themeit=THEME2)
		addFile('[COLOR red][B][BORRAR][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		fold = glob.glob(os.path.join(ADDOND, '*/'))
		for folder in sorted(fold, key = lambda x: x):
			foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
			icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
			fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
			folderdisplay = foldername
			replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR green][SCRIPT] [/COLOR]', 'service.':'[COLOR green][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
			for rep in replace:
				folderdisplay = folderdisplay.replace(rep, replace[rep])
			if foldername in EXCLUDES: folderdisplay = '[COLOR green][B][PROTEGIDO][/B][/COLOR] %s' % folderdisplay
			else: folderdisplay = '[COLOR red][B][BORRAR][/B][/COLOR] %s' % folderdisplay
			addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
	else:
		addFile('No Addon data folder found.', '', themeit=THEME3)
	setView('files', 'viewType')

def enableAddons():
	addFile("[I][B][COLOR red]!!Alerta: Deshabilitar algunos addons puede causar problemas!![/COLOR][/B][/I]", '', icon=ICONMAINT)
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	x = 0
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		if foldername in DEFAULTPLUGINS: continue
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			x += 1
			fold   = folder.replace(ADDONS, '')[1:-1]
			f      = open(addonxml)
			a      = f.read().replace('\n','').replace('\r','').replace('\t','')
			match  = wiz.parseDOM(a, 'addon', ret='id')
			match2 = wiz.parseDOM(a, 'addon', ret='name')
			try:
				pluginid = match[0]
				name = match2[0]
			except:
				continue
			try:
				add    = xbmcaddon.Addon(id=pluginid)
				state  = "[COLOR green][Activado][/COLOR]"
				goto   = "false"
			except:
				state  = "[COLOR red][Desactivado][/COLOR]"
				goto   = "true"
				pass
			icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
			fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
			addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
			f.close()
	if x == 0:
		addFile("No Addons Found to Enable or Disable.", '', icon=ICONMAINT)
	setView('files', 'viewType')

def changeFeq():
	feq        = ['Every Startup', 'Every Day', 'Every Three Days', 'Every Weekly']
	change     = DIALOG.select("[COLOR %s]How often would you list to Auto Clean on Startup?[/COLOR]" % COLOR2, feq)
	if not change == -1: 
		wiz.setS('autocleanfeq', str(change))
		wiz.LogNotify('[COLOR %s]Auto Clean Up[/COLOR]' % COLOR1, '[COLOR %s]Fequency Now %s[/COLOR]' % (COLOR2, feq[change]))

def developer():
	addFile('Convert Text Files to 0.1.7',         'converttext',           themeit=THEME1)
	addFile('Test Notifications',                  'testnotify',            themeit=THEME1)
	addFile('Test Update',                         'testupdate',            themeit=THEME1)
	addFile('Test First Run',                      'testfirst',             themeit=THEME1)
	addFile('Test First Run Settings',             'testfirstrun',          themeit=THEME1)
	addFile('Test APk',             'testapk',          themeit=THEME1)
	
	setView('files', 'viewType')

###########################
###### Build Install ######
###########################
def buildWizard(name, type, theme=None, over=False):
	if over == False:
		testbuild = wiz.checkBuild(name, 'url')
		if testbuild == False:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Unabled to find build[/COLOR]" % COLOR2)
			return
		testworking = wiz.workingURL(testbuild)
		if testworking == False:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Build Zip Error: %s[/COLOR]" % (COLOR2, testworking))
			return
	if type == 'gui':
		if name == BUILDNAME:
			if over == True: yes = 1
			else: yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to apply the guifix for:' % COLOR2, '[COLOR %s]%s[/COLOR]?[/COLOR]' % (COLOR1, name), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Apply Fix[/COLOR][/B]')
		else: 
			yes = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "[COLOR %s][COLOR %s]%s[/COLOR] community build is not currently installed." % (COLOR2, COLOR1, name), "Would you like to apply the guiFix anyways?.[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Apply Fix[/COLOR][/B]')
		if yes:
			buildzip = wiz.checkBuild(name,'gui')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Invalid Zip Url![/COLOR]' % COLOR2); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'[COLOR %s][B]Downloading GuiFix:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Espera')
			lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
			DP.update(0, title,'', 'Espera')
			extract.all(lib,USERDATA,DP, title=title)
			DP.close()
			wiz.defaultSkin()
			wiz.lookandFeelData('save')
			if INSTALLMETHOD == 1: todo = 1
			elif INSTALLMETHOD == 2: todo = 0
			else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Gui fix has been installed.  Would you like to Reload the profile or Force Close Kodi?[/COLOR]" % COLOR2, yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR green]Force Close[/COLOR][/B]")
			if todo == 1: wiz.reloadFix()
			else: DIALOG.ok(ADDONTITLE, "[COLOR %s]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]" % COLOR2); wiz.killxbmc('true')
		else:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Cancelled![/COLOR]' % COLOR2)
	elif type == 'fresh':
		freshStart(name)
	elif type == 'normal':
		if url == 'normal':
			yes_pressed = DIALOG.yesno("%s - [COLOR yellow]INSTALACION DE PARCHE[/COLOR]" % ADDONTITLE, '[COLOR %s]Vas a instalar un Parche para la Build' % COLOR2, 'Kodi %s no se limpiara, si limpias Kodi %s el parche no funcionaria correctamente.' % (wiz.checkBuild(name, 'kodi'), KODIV), 'Quieres instalar el parche: [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]',yeslabel='[B][COLOR green]Si, Instalar[/COLOR][/B]')
		else:
			if not over == False: yes_pressed = 1
			else: yes_pressed = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres descargar e instalar?:' % COLOR2, '[COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]',yeslabel='[B][COLOR green]Si, Instalar[/COLOR][/B]')
		if yes_pressed:
			wiz.clearS('build')
			buildzip = wiz.checkBuild(name, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Instalacion Build: Invalid Zip Url![/COLOR]' % COLOR2); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'[COLOR %s][B]Descargando:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')),'', 'Espera')
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			title = '[COLOR %s][B]Instalando:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version'))
			DP.update(0, title,'', 'Espera')
			percent, errors, error = extract.all(lib,HOME,DP, title=title)
			if int(float(percent)) > 0:
				wiz.fixmetas()
				wiz.lookandFeelData('save')
				wiz.defaultSkin()
				#wiz.addonUpdates('set')
				wiz.setS('buildname', name)
				wiz.setS('buildversion', wiz.checkBuild( name,'version'))
				wiz.setS('buildtheme', '')
				wiz.setS('latestversion', wiz.checkBuild( name,'version'))
				wiz.setS('lastbuildcheck', str(NEXTCHECK))
				wiz.setS('installed', 'true')
				wiz.setS('extract', str(percent))
				wiz.setS('errors', str(errors))
				wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
				try: os.remove(lib)
				except: pass
				if int(float(errors)) > 0:
					yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild( name,'version')), 'Completado: [COLOR %s]%s%s[/COLOR] [Errores:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Quieres ver los errores?[/COLOR]', nolabel='[B][COLOR red]No Gracias[/COLOR][/B]', yeslabel='[B][COLOR green]Ver Errores[/COLOR][/B]')
					if yes:
						if isinstance(errors, unicode):
							error = error.encode('utf-8')
						wiz.TextBox(ADDONTITLE, error)
				DP.close()
				themefile = wiz.themeCount(name)
				if not themefile == False:
					buildWizard(name, 'theme')
				if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
				if INSTALLMETHOD == 1: todo = 1
				elif INSTALLMETHOD == 2: todo = 0
				else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres[COLOR %s] Forzar el cierre[/COLOR] de kodi o [COLOR %s]Recargar Perfil[/COLOR]? La opcion recomendada es Forzar Cierre.[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Recargar Perfil[/COLOR][/B]", nolabel="[B][COLOR green]Forzar Cierre[/COLOR][/B]")
				if todo == 1: wiz.reloadFix()
				else: wiz.killxbmc(True)
			else:
				if isinstance(errors, unicode):
					error = error.encode('utf-8')
				wiz.TextBox("%s: Error Installing Build" % ADDONTITLE, error)
		else:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Instalacion de Parche: Cancelada![/COLOR]' % COLOR2)
	elif type == 'theme':
		if theme == None:
			themefile = wiz.checkBuild(name, 'theme')
			themelist = []
			if not themefile == 'http://' and wiz.workingURL(themefile) == True:
				themelist = wiz.themeCount(name, False)
				if len(themelist) > 0:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Build [COLOR %s]%s[/COLOR] comes with [COLOR %s]%s[/COLOR] different themes" % (COLOR2, COLOR1, name, COLOR1, len(themelist)), "Would you like to install one now?[/COLOR]", yeslabel="[B][COLOR green]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]"):
						wiz.log("Theme List: %s " % str(themelist))
						ret = DIALOG.select(ADDONTITLE, themelist)
						wiz.log("Theme install selected: %s" % ret)
						if not ret == -1: theme = themelist[ret]; installtheme = True
						else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
			else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: None Found![/COLOR]' % COLOR2)
		else: installtheme = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to install the theme:' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, theme), 'for [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), yeslabel="[B][COLOR green]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]")
		if installtheme:
			themezip = wiz.checkTheme(name, theme, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(themezip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Invalid Zip Url![/COLOR]' % COLOR2); return False
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme),'', 'Espera')
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(themezip, lib, DP)
			xbmc.sleep(500)
			DP.update(0,"", "Installing %s " % name)
			test = False
			if url not in ["fresh", "normal"]:
				test = testTheme(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
				test2 = testGui(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
				if test == True:
					wiz.lookandFeelData('save')
					skin     = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
					gotoskin = xbmc.getSkinDir()
					#if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Installing the theme [COLOR %s]%s[/COLOR] requires the skin to be swaped back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, theme, COLOR1, skin[5:]), "Would you like to switch the skin?[/COLOR]", yeslabel="[B][COLOR green]Switch Skin[/COLOR][/B]", nolabel="[B][COLOR red]Don't Switch[/COLOR][/B]"):
					skinSwitch.swapSkins(skin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)
					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return
					xbmc.sleep(500)
			title = '[COLOR %s][B]Installing Theme:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme)
			DP.update(0, title,'', 'Please Wait')
			percent, errors, error = extract.all(lib,HOME,DP, title=title)
			wiz.setS('buildtheme', theme)
			wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
			DP.close()
			if url not in ["fresh", "normal"]: 
				wiz.forceUpdate()
				if KODIV >= 17: wiz.kodi17Fix()
				if test2 == True:
					wiz.lookandFeelData('save')
					wiz.defaultSkin()
					gotoskin = wiz.getS('defaultskin')
					skinSwitch.swapSkins(gotoskin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)

					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					wiz.lookandFeelData('restore')
				elif test == True:
					skinSwitch.swapSkins(gotoskin)
					x = 0
					xbmc.sleep(1000)
					while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
						x += 1
						xbmc.sleep(200)

					if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
						wiz.ebi('SendClick(11)')
					else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return
					wiz.lookandFeelData('restore')
				else:
					wiz.ebi("ReloadSkin()")
					xbmc.sleep(1000)
					wiz.ebi("Container.Refresh") 
		else:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2)

def thirdPartyInstall(name, url):
	if not wiz.workingURL(url):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Url del zip invalida[/COLOR]' % COLOR2); return
	type = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Como quieres hacer la instalacion? [COLOR %s]Instalacion CON limpieza[/COLOR] o [COLOR %s]Instalacion SIN Limpieza[/COLOR] para:[/COLOR]" % (COLOR2, COLOR1, COLOR1), "[COLOR %s]%s[/COLOR]" % (COLOR1, name), yeslabel="[B][COLOR green]Con Limpieza[/COLOR][/B]", nolabel="[B][COLOR red]Sin Limpieza[/COLOR][/B]")
	if type == 1:
		freshStart('third', True)
	wiz.clearS('build')
	zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[COLOR %s][B]Descargando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Espera')
	lib=os.path.join(PACKAGES, '%s.zip' % zipname)
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	xbmc.sleep(500)
	title = '[COLOR %s][B]Instalando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', 'Please Wait')
	percent, errors, error = extract.all(lib,HOME,DP, title=title)
	if int(float(percent)) > 0:
		wiz.fixmetas()
		wiz.lookandFeelData('save')
		wiz.defaultSkin()
		#wiz.addonUpdates('set')
		wiz.setS('installed', 'true')
		wiz.setS('extract', str(percent))
		wiz.setS('errors', str(errors))
		wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
		try: os.remove(lib)
		except: pass
		if int(float(errors)) > 0:
			yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), 'Completado: [COLOR %s]%s%s[/COLOR] [Errores:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Quieres ver los errores?[/COLOR]', nolabel='[B][COLOR red]No[/COLOR][/B]',yeslabel='[B][COLOR green]Ver Errores[/COLOR][/B]')
			if yes:
				if isinstance(errors, unicode):
					error = error.encode('utf-8')
				wiz.TextBox(ADDONTITLE, error)
	DP.close()
	if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres [COLOR %s]Forzar el cierre[/COLOR] de kodi o [COLOR %s]Recargar perfil[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR green]Recargar Perfil[/COLOR][/B]", nolabel="[B][COLOR red]Forzar Cierre[/COLOR][/B]")
	if todo == 1: wiz.reloadFix()
	else: wiz.killxbmc(True)

def testTheme(path):
	zfile = zipfile.ZipFile(path)
	for item in zfile.infolist():
		if '/settings.xml' in item.filename:
			return True
	return False

def testGui(path):
	zfile = zipfile.ZipFile(path)
	for item in zfile.infolist():
		if '/guisettings.xml' in item.filename:
			return True
	return False

def apkInstaller(apk, url):
	wiz.log(apk)
	wiz.log(url)
	if wiz.platform() == 'android':
		yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres descargar e instalar:" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, apk), yeslabel="[B][COLOR green]Descargar[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")
		if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Instalacion cancelada[/COLOR]' % COLOR2); return
		display = apk
		if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
		if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Instalador App: Url invalida![/COLOR]' % COLOR2); return
		DP.create(ADDONTITLE,'[COLOR %s][B]Descargando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display),'', 'Espera')
		lib=os.path.join(PACKAGES, "%s.apk" % apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
		try: os.remove(lib)
		except: pass
		downloader.download(url, lib, DP)
		xbmc.sleep(100)
		DP.close()
		notify.apkInstaller(apk)
		wiz.ebi('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
	else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Ningun dispositivo Android[/COLOR]' % COLOR2)

###########################
###### Misc Functions######
###########################

def createMenu(type, add, name):
	if   type == 'saveaddon':
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Guardar %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restaurar %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Limpiar %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'save'    :
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Registrar %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Guardar %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restaurar %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Importar %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Limpiar Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'install'  :
		menu_items=[]
		name2 = urllib.quote_plus(name)
		menu_items.append((THEME2 % name,                                'RunAddon(%s, ?mode=viewbuild&name=%s)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Fresh Install',                     'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Normal Install',                    'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Apply guiFix',                      'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Build Information',                 'RunPlugin(plugin://%s/?mode=buildinfo&name=%s)'  % (ADDON_ID, name2)))
	menu_items.append((THEME2 % '%s Settings' % ADDONTITLE,              'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
	return menu_items


def playVideo(url):
	if 'watch?v=' in url:
		a, b = url.split('?')
		find = b.split('&')
		for item in find:
			if item.startswith('v='):
				url = item[2:]
				break
			else: continue
	elif 'embed' in url or 'youtu.be' in url:
		a = url.split('/')
		if len(a[-1]) > 5:
			url = a[-1]
		elif len(a[-2]) > 5:
			url = a[-2]
	wiz.log("YouTube URL: %s" % url)
	yt.PlayVideo(url)

def viewLogFile():
	mainlog = wiz.Grab_Log(True)
	oldlog  = wiz.Grab_Log(True, True)
	which = 0; logtype = mainlog
	if not oldlog == False and not mainlog == False:
		which = DIALOG.select(ADDONTITLE, ["Ver %s" % mainlog.replace(LOG, ""), "Ver %s" % oldlog.replace(LOG, "")])
		if which == -1: wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Ver Log Cancelado![/COLOR]' % COLOR2); return
	elif mainlog == False and oldlog == False:
		wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Log no encontrado![/COLOR]' % COLOR2)
		return
	elif not mainlog == False: which = 0
	elif not oldlog == False: which = 1
	
	logtype = mainlog if which == 0 else oldlog
	msg     = wiz.Grab_Log(False) if which == 0 else wiz.Grab_Log(False, True)
	
	wiz.TextBox("%s - %s" % (ADDONTITLE, logtype), msg)

def errorChecking(log=None, count=None, all=None):
	if log == None:
		mainlog = wiz.Grab_Log(True)
		oldlog  = wiz.Grab_Log(True, True)
		if not oldlog == False and not mainlog == False:
			which = DIALOG.select(ADDONTITLE, ["Ver %s: %s error(es)" % (mainlog.replace(LOG, ""), errorChecking(mainlog, True, True)), "Ver %s: %s error(es)" % (oldlog.replace(LOG, ""), errorChecking(oldlog, True, True))])
			if which == -1: wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Ver Log Cancelado![/COLOR]' % COLOR2); return
		elif mainlog == False and oldlog == False:
			wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Log No encontrado![/COLOR]' % COLOR2)
			return
		elif not mainlog == False: which = 0
		elif not oldlog == False: which = 1
		log = mainlog if which == 0 else oldlog
	if log == False:
		if count == None:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Log no encontrado[/COLOR]" % COLOR2)
			return False
		else: 
			return 0
	else:
		if os.path.exists(log):
			f = open(log,mode='r'); a = f.read().replace('\n', '').replace('\r', ''); f.close()
			match = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(a)
			if not count == None:
				if all == None: 
					x = 0
					for item in match:
						if ADDON_ID in item: x += 1
					return x
				else: return len(match)
			if len(match) > 0:
				x = 0; msg = ""
				for item in match:
					if all == None and not ADDON_ID in item: continue
					else: 
						x += 1
						msg += "[COLOR red]Error Number %s[/COLOR]\n(PythonToCppException) : -->Python callback/script returned the following error<--%s-->End of Python script error report<--\n\n" % (x, item.replace('                                          ', '\n').replace('\\\\','\\').replace(HOME, ''))
				if x > 0:
					wiz.TextBox(ADDONTITLE, msg)
				else: wiz.LogNotify(ADDONTITLE, "No Errors Found in Log")
			else: wiz.LogNotify(ADDONTITLE, "No Errors Found in Log")
		else: wiz.LogNotify(ADDONTITLE, "Log File not Found")

ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

def LogViewer(default=None):
	class LogViewer(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.default = kwargs['default']

		def onInit(self):
			self.title      = 101
			self.msg        = 102
			self.scrollbar  = 103
			self.upload     = 201
			self.kodi       = 202
			self.kodiold    = 203
			self.wizard     = 204 
			self.okbutton   = 205 
			f = open(self.default, 'r')
			self.logmsg = f.read()
			f.close()
			self.titlemsg = "%s: %s" % (ADDONTITLE, self.default.replace(LOG, '').replace(ADDONDATA, ''))
			self.showdialog()

		def showdialog(self):
			self.getControl(self.title).setLabel(self.titlemsg)
			self.getControl(self.msg).setText(wiz.highlightText(self.logmsg))
			self.setFocusId(self.scrollbar)
			
		def onClick(self, controlId):
			if   controlId == self.okbutton: self.close()
			elif controlId == self.upload: self.close(); uploadLog.Main()
			elif controlId == self.kodi:
				newmsg = wiz.Grab_Log(False)
				filename = wiz.Grab_Log(True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ADDONTITLE
					self.getControl(self.msg).setText("Log File Does Not Exists!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.kodiold:  
				newmsg = wiz.Grab_Log(False, True)
				filename = wiz.Grab_Log(True, True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ADDONTITLE
					self.getControl(self.msg).setText("Log File Does Not Exists!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.wizard:
				newmsg = wiz.Grab_Log(False, False, True)
				filename = wiz.Grab_Log(True, False, True)
				if newmsg == False:
					self.titlemsg = "%s: View Log Error" % ADDONTITLE
					self.getControl(self.msg).setText("Log File Does Not Exists!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(ADDONDATA, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
		
		def onAction(self, action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()
	if default == None: default = wiz.Grab_Log(True)
	lv = LogViewer( "LogViewer.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', default=default)
	lv.doModal()
	del lv

def removeAddon(addon, name, over=False):
	if not over == False:
		yes = 1
	else: 
		yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres borrar el addon:'% COLOR2, 'Nombre: [COLOR %s]%s[/COLOR]' % (COLOR1, name), 'ID: [COLOR %s]%s[/COLOR][/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR green]Borrar Addon[/COLOR][/B]', nolabel='[B][COLOR red]No Borrar[/COLOR][/B]')
	if yes == 1:
		folder = os.path.join(ADDONS, addon)
		wiz.log("Removing Addon %s" % addon)
		wiz.cleanHouse(folder)
		xbmc.sleep(200)
		try: shutil.rmtree(folder)
		except Exception ,e: wiz.log("Error removing %s" % addon, xbmc.LOGNOTICE)
		removeAddonData(addon, name, over)
	if over == False:
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Borrado[/COLOR]" % (COLOR2, name))

def removeAddonData(addon, name=None, over=False):
	if addon == 'all':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres borrar [COLOR %s]TODAS[/COLOR] las carpetas de Addon_Data?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Borrar Data[/COLOR][/B]', nolabel='[B][COLOR red]No Borrar[/COLOR][/B]'):
			wiz.cleanHouse(ADDOND)
		else: wiz.LogNotify('[COLOR %s]Borrar Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelado![/COLOR]' % COLOR2)
	elif addon == 'uninstalled':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres borrar [COLOR %s]TODAS[/COLOR] las carpetas de addon_data de addons desinstalados?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Borrar Data[/COLOR][/B]', nolabel='[B][COLOR red]No Borrar[/COLOR][/B]'):
			total = 0
			for folder in glob.glob(os.path.join(ADDOND, '*')):
				foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify('[COLOR %s]Carpetas de Addons desinstalados[/COLOR]' % COLOR1, '[COLOR %s]%s Carpeta(s) Borrada(s)[/COLOR]' % (COLOR2, total))
		else: wiz.LogNotify('[COLOR %s]Borrar Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelado![/COLOR]' % COLOR2)
	elif addon == 'empty':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres borrar [COLOR %s]TODAS[/COLOR] las carpetas vacias de Addon_Data?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Borrar Data[/COLOR][/B]', nolabel='[B][COLOR red]No Borrar[/COLOR][/B]'):
			total = wiz.emptyfolder(ADDOND)
			wiz.LogNotify('[COLOR %s]Borrar Carpetas vacias[/COLOR]' % COLOR1, '[COLOR %s]%s Carpeta(s) Borrada(s)[/COLOR]' % (COLOR2, total))
		else: wiz.LogNotify('[COLOR %s]Borrar carpetas vacias[/COLOR]' % COLOR1, '[COLOR %s]Cancelado![/COLOR]' % COLOR2)
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("[COLOR %s]Addon Protegido[/COLOR]" % COLOR1, "[COLOR %s]No esta permitido borrar su Addon_Data[/COLOR]" % COLOR2)
		elif os.path.exists(addon_data):  
			if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres borrar la carpeta addon_data de:[/COLOR]' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR green]Borrar Data[/COLOR][/B]', nolabel='[B][COLOR red]No Borrar[/COLOR][/B]'):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error borrando: %s" % addon_data)
			else: 
				wiz.log('Addon data for %s was not removed' % addon)
	wiz.refresh()

def restoreit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Restauracion Cancelada[/COLOR]" % COLOR2); return
	if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
		wiz.skinToDefault()
	wiz.restoreLocal(type)

def restoreextit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Restauracion Externa Cancelada[/COLOR]" % COLOR2); return
	wiz.restoreExternal(type)

def buildInfo(name):
	if wiz.workingURL(BUILDFILE) == True:
		if wiz.checkBuild(name, 'url'):
			name, version, url, gui, kodi, theme, icon, fanart, preview, adult, description = wiz.checkBuild(name, 'all')
			adult = 'Yes' if adult.lower() == 'yes' else 'No'
			msg  = "[COLOR %s]Nombre de la Build:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
			msg += "[COLOR %s]Version de la Build:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
			if not theme == "http://":
				themecount = wiz.themeCount(name, False)
				msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
			msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
			msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
			msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)
			wiz.TextBox(ADDONTITLE, msg)
		else: wiz.log("Invalid Build Name!")
	else: wiz.log("Build text file not working: %s" % WORKINGURL)

def buildVideo(name):
	if wiz.workingURL(BUILDFILE) == True:
		videofile = wiz.checkBuild(name, 'preview')
		if videofile and not videofile == 'http://': playVideo(videofile)
		else: wiz.log("[%s]Unable to find url for video preview" % name)
	else: wiz.log("Build text file not working: %s" % WORKINGURL)

def dependsList(plugin):
	addonxml = os.path.join(ADDONS, plugin, 'addon.xml')
	if os.path.exists(addonxml):
		source = open(addonxml,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		items  = []
		for depends in match:
			if not 'xbmc.python' in depends:
				items.append(depends)
		return items
	return []

def manageSaveData(do):
	if do == 'import':
		TEMP = os.path.join(ADDONDATA, 'temp')
		if not os.path.exists(TEMP): os.makedirs(TEMP)
		source = DIALOG.browse(1, '[COLOR %s]Select the location of the SaveData.zip[/COLOR]' % COLOR2, 'files', '.zip', False, False, HOME)
		if not source.endswith('.zip'):
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
			return
		tempfile = os.path.join(MYBUILDS, 'SaveData.zip')
		goto = xbmcvfs.copy(source, tempfile)
		wiz.log("%s" % str(goto))
		extract.all(xbmc.translatePath(tempfile), TEMP)
		x = 0
		wiz.cleanHouse(TEMP)
		wiz.removeFolder(TEMP)
		os.remove(tempfile)
		if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Failed[/COLOR]" % COLOR2)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Completa[/COLOR]" % COLOR2)
		if source == mybuilds:
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))
		else:
			try:
				xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'SaveData.zip')))
			except:
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))

###########################
###### Fresh Install ######
###########################
def freshStart(install=None, over=False):
	if over == True: yes_pressed = 1
	elif install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres hacer una limpieza total de Kodi" % COLOR2, "De su configuracion, de los addons y sus ajustes?", "Antes de instalar el backup local?[/COLOR]", nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	elif install: yes_pressed=DIALOG.yesno("%s - [COLOR green]INSTALACION DE BUILD[/COLOR]" % ADDONTITLE, "[COLOR %s]Se va a realizar una limpieza total de Kodi, antes de instalar la Build." % COLOR2, "Recuerda activar, guardar la videoteca y fuentes desde Conservar data", "Quieres continuar con la instalacion de [COLOR %s]%s[/COLOR]" % (COLOR1, install), nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	else: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres hacer una limpieza total de Kodi" % COLOR2, "De su configurtacion, de los addons y sus configuraciones?[/COLOR]", nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	if yes_pressed:
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
			#yes=DIALOG.yesno(ADDONTITLE, "[COLOR %s]The skin needs to be set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, skin[5:]), "Before doing a fresh install to clear all Texture files,", "Would you like us to do that for you?[/COLOR]", yeslabel="[B][COLOR green]Switch Skins[/COLOR][/B]", nolabel="[B][COLOR red]I'll Do It[/COLOR][/B]";
			#if yes:
			skinSwitch.swapSkins(skin)
			x = 0
			xbmc.sleep(1000)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
				x += 1
				xbmc.sleep(200)
				wiz.ebi('SendAction(Select)')
			if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				wiz.ebi('SendClick(11)')
			else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return False
			xbmc.sleep(1000)
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Failed![/COLOR]' % COLOR2)
			return
		wiz.addonUpdates('set')
		xbmcPath=os.path.abspath(HOME)
		DP.create(ADDONTITLE,"[COLOR %s]Calculando archivos y carpetas" % COLOR2,'', 'Espera![/COLOR]')
		total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
		DP.update(0, "[COLOR %s]Gathering Excludes list." % COLOR2)
		EXCLUDES.append('MisBuilds')
		EXCLUDES.append('archive_cache')
		if KEEPREPOS == 'true':
			repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
			for item in repos:
				repofolder = os.path.split(item[:-1])[1]
				if not repofolder == EXCLUDES:
					EXCLUDES.append(repofolder)
		if KEEPSUPER == 'true':
			EXCLUDES.append('plugin.program.super.favourites')
		if KEEPWHITELIST == 'true':
			pvr = ''
			whitelist = wiz.whiteList('read')
			if len(whitelist) > 0:
				for item in whitelist:
					try: name, id, fold = item
					except: pass
					if fold.startswith('pvr'): pvr = id 
					depends = dependsList(fold)
					for plug in depends:
						if not plug in EXCLUDES:
							EXCLUDES.append(plug)
						depends2 = dependsList(plug)
						for plug2 in depends2:
							if not plug2 in EXCLUDES:
								EXCLUDES.append(plug2)
					if not fold in EXCLUDES:
						EXCLUDES.append(fold)
				if not pvr == '': wiz.setS('pvrclient', fold)
		if wiz.getS('pvrclient') == '':
			for item in EXCLUDES:
				if item.startswith('pvr'):
					wiz.setS('pvrclient', item)
		DP.update(0, "[COLOR %s]Limpiando archivos y carpetas:" % COLOR2)
		latestAddonDB = wiz.latestDB('Addons')
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				del_file += 1
				fold = root.replace('/','\\').split('\\')
				x = len(fold)-1
				if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep Sources: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'MyVideos107.db' and fold[-1] == 'Database' and KEEPMYVIDEOS == 'true': wiz.log("Keep MyVideos: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep Favourites: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep Profiles: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name in LOGFILES: wiz.log("Keep Log File: %s" % name, xbmc.LOGNOTICE)
				elif name.endswith('.db'):
					try:
						if name == latestAddonDB and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV), xbmc.LOGNOTICE)
						else: os.remove(os.path.join(root,name))
					except Exception, e: 
						if not name.startswith('Textures13'):
							wiz.log('Failed to delete, Purging DB', xbmc.LOGNOTICE)
							wiz.log("-> %s" % (str(e)), xbmc.LOGNOTICE)
							wiz.purgeDb(os.path.join(root,name))
				else:
					DP.update(int(wiz.percentage(del_file, total_files)), '', '[COLOR %s]Archivo: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '')
					try: os.remove(os.path.join(root,name))
					except Exception, e: 
						wiz.log("Error removing %s" % os.path.join(root, name), xbmc.LOGNOTICE)
						wiz.log("-> / %s" % (str(e)), xbmc.LOGNOTICE)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
				return False
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				DP.update(100, '', 'Cleaning Up Empty Folder: [COLOR %s]%s[/COLOR]' % (COLOR1, name), '')
				if name not in ["Database","userdata","temp","addons","addon_data"]:
					shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
				return False
		DP.close()
		wiz.clearS('build')
		if over == True:
			return True
		elif install == 'restore': 
			return True
		elif install: 
			buildWizard(install, 'normal', over=True)
		else:
			if INSTALLMETHOD == 1: todo = 1
			elif INSTALLMETHOD == 2: todo = 0
			else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR green]Force Close[/COLOR][/B]")
			if todo == 1: wiz.reloadFix('fresh')
			else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
	else: 
		if not install == 'restore':
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Instalar Build: Cancelada![/COLOR]' % COLOR2)
			wiz.refresh()

#############################
###DELETE CACHE##############
####THANKS GUYS @ NaN #######
def clearCache():
	if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR green]Clear Cache[/COLOR][/B]'):
		wiz.clearCache()
		#clearThumb()

def totalClean():
	if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Quieres limpiar el cache los paquetes y las imagenes?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]Cancelar Proceso[/COLOR][/B]',yeslabel='[B][COLOR green]Limpiar todo[/COLOR][/B]'):
		wiz.clearCache()
		wiz.clearPackages('total')
		clearThumb('total')

def clearThumb(type=None):
	latest = wiz.latestDB('Textures')
	if not type == None: choice = 1
	else: choice = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to delete the %s and Thumbnails folder?' % (COLOR2, latest), "They will repopulate on the next startup[/COLOR]", nolabel='[B][COLOR red]Don\'t Delete[/COLOR][/B]', yeslabel='[B][COLOR green]Delete Thumbs[/COLOR][/B]')
	if choice == 1:
		try: wiz.removeFile(os.join(DATABASE, latest))
		except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
		wiz.removeFolder(THUMBS)
		#if not type == 'total': wiz.killxbmc()
	else: wiz.log('Clear thumbnames cancelled')
	wiz.redoThumbs()

def purgeDb():
	DB = []; display = []
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIV >= 16: 
		choice = DIALOG.multiselect("[COLOR %s]Elige el archivo DB a Purgar[/COLOR]" % COLOR2, display)
		if choice == None: wiz.LogNotify("[COLOR %s]Purgar Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Purgar Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = DIALOG.select("[COLOR %s]Elige el archivo DB a Purgar[/COLOR]" % COLOR2, display)
		if choice == -1: wiz.LogNotify("[COLOR %s]Purgar Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		else: wiz.purgeDb(DB[purge])

##########################
### DEVELOPER MENU #######
##########################
def testnotify():
	url = wiz.workingURL(NOTIFICATION)
	if url == True:
		try:
			id, msg = wiz.splitNotify(NOTIFICATION)
			if id == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Notification: Not Formated Correctly[/COLOR]" % COLOR2); return
			notify.notification(msg, True)
		except Exception, e:
			wiz.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
	else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Invalid URL for Notification[/COLOR]" % COLOR2)

def testupdate():
	if BUILDNAME == "":
		notify.updateWindow()
	else:
		notify.updateWindow(BUILDNAME, BUILDVERSION, BUILDLATEST, wiz.checkBuild(BUILDNAME, 'icon'), wiz.checkBuild(BUILDNAME, 'fanart'))

def testfirst():
	notify.firstRun()

def testfirstRun():
	notify.firstRunSettings()

###########################
## Making the Directory####
###########################

def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]

		return param

params=get_params()
url=None
name=None
mode=None

try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass

wiz.log('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ Url : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
	if wiz.getS('auto-view')=='true':
		views = wiz.getS(viewType)
		if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
		if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
		wiz.ebi("Container.SetViewMode(%s)" %  views)

if   mode==None             : index()

elif mode=='wizardupdate'   : wiz.wizardUpdate()
elif mode=='builds'         : buildMenu()
elif mode=='viewbuild'      : viewBuild(name)
elif mode=='buildinfo'      : buildInfo(name)
elif mode=='buildpreview'   : buildVideo(name)
elif mode=='install'        : buildWizard(name, url)
elif mode=='theme'          : buildWizard(name, mode, url)
elif mode=='viewthirdparty' : viewThirdList(name)
elif mode=='installthird'   : thirdPartyInstall(name, url)
elif mode=='editthird'      : editThirdParty(name); wiz.refresh()
elif mode=='maint'          : maintMenu(name)
elif mode=='kodi17fix'      : wiz.kodi17Fix()
elif mode=='advancedsetting': advancedWindow(name)
elif mode=='autoadvanced'   : showAutoAdvanced(); wiz.refresh()
elif mode=='removeadvanced' : removeAdvanced(); wiz.refresh()
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='backupaddon'    : wiz.backUpOptions('addondata')
elif mode=='oldThumbs'      : wiz.oldThumbs()
elif mode=='clearbackup'    : wiz.cleanupBackup()
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='currentsettings': viewAdvanced()
elif mode=='fullclean'      : totalClean(); wiz.refresh()
elif mode=='clearcache'     : clearCache(); wiz.refresh()
elif mode=='clearpackages'  : wiz.clearPackages(); wiz.refresh()
elif mode=='clearcrash'     : wiz.clearCrash(); wiz.refresh()
elif mode=='clearthumb'     : clearThumb(); wiz.refresh()
elif mode=='checksources'   : wiz.checkSources(); wiz.refresh()
elif mode=='checkrepos'     : wiz.checkRepos(); wiz.refresh()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceprofile'   : wiz.reloadProfile(wiz.getInfo('System.ProfileName'))
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='forceskin'      : wiz.ebi("ReloadSkin()"); wiz.refresh()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='enableaddons'   : enableAddons()
elif mode=='toggleaddon'    : wiz.toggleAddon(name, url); wiz.refresh()
elif mode=='togglecache'    : toggleCache(name); wiz.refresh()
elif mode=='toggleadult'    : wiz.toggleAdult(); wiz.refresh()
elif mode=='changefeq'      : changeFeq(); wiz.refresh()
elif mode=='viewlog'        : LogViewer()
elif mode=='viewwizlog'     : LogViewer(WIZLOG)
elif mode=='viewerrorlog'   : errorChecking(all=True)
elif mode=='clearwizlog'    : f = open(WIZLOG, 'w'); f.close(); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Log Cleared![/COLOR]" % COLOR2)
elif mode=='purgedb'        : purgeDb()
elif mode=='fixaddonupdate' : fixUpdate()
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Addon_Data reset[/COLOR]" % COLOR2)
elif mode=='systeminfo'     : systemInfo()
elif mode=='restorezip'     : restoreit('build')
elif mode=='restoregui'     : restoreit('gui')
elif mode=='restoreaddon'   : restoreit('addondata')
elif mode=='restoretheme'   : restoreit('theme')
elif mode=='restoreextzip'  : restoreextit('build')
elif mode=='restoreextgui'  : restoreextit('gui')
elif mode=='restoreextaddon': restoreextit('addondata')
elif mode=='writeadvanced'  : writeAdvanced(name, url)

elif mode=='apk'            : apkMenu(name)
elif mode=='apkscrape'      : apkScraper(name)
elif mode=='apkinstall'     : apkInstaller(name, url)

elif mode=='youtube'        : youtubeMenu(name)
elif mode=='viewVideo'      : playVideo(url)

elif mode=='addons'         : addonMenu(name)
elif mode=='addoninstall'   : addonInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); wiz.refresh()
elif mode=='managedata'     : manageSaveData(name)
elif mode=='whitelist'      : wiz.whiteList(name)

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(name); wiz.refresh()
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); wiz.refresh()

elif mode=='developer'      : developer()
elif mode=='converttext'    : wiz.convertText()
elif mode=='testnotify'     : testnotify()
elif mode=='testupdate'     : testupdate()
elif mode=='testfirst'      : testfirst()
elif mode=='testfirstrun'   : testfirstRun()
elif mode=='testapk'        : notify.apkInstaller('SPMC')

xbmcplugin.endOfDirectory(int(sys.argv[1]))