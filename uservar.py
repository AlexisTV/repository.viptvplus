import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[COLOR cyan]VIPTV[/COLOR][COLOR crimson][B] Astro[/B][/COLOR]'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'http://tvandroidianox.com/Wizard2/wizard.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'https://stva.zriel.ga/wizard/txt/apk.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'Video Tutoriales'
YOUTUBEFILE    = 'http://tvandroidianox.com/Wizard/Video%20Guias%20VipTV0.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'https://stva.zriel.ga/wizard/txt/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'https://stva.zriel.ga/wizard/txt/Advanced.txt'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################

ICONBUILDS     = 'http://tvandroidianox.com/Wizard2/icon%20Instalar%20y%20Actualizar%20VipTV.jpg'
ICONMAINT      = 'http://tvandroidianox.com/Wizard/icono%20de%20mantenimiento%20viptv.png'
ICONAPK        = 'http://www.lookingglass.rocks/images/forks.jpg'
ICONADDONS     = 'http://tvandroidianox.com/Wizard/Icon%20addon%20viptv%20descaga.png'
ICONYOUTUBE    = 'http://tvandroidianox.com/Wizard/icon%20viptv%20videos%20guias%20y%20tutoriales.png'
ICONSAVE       = 'http://tvandroidianox.com/Wizard/icon%20save%20viptv.png'
ICONTRAKT      = 'http://tvandroidianox.com/Wizard/publicidad.jpg'
ICONREAL       = 'http://tvandroidianox.com/Wizard/publicidad.jpg'
ICONLOGIN      = 'http://www.lookingglass.rocks/images/login.jpg'
ICONCONTACT    = 'https://stva.zriel.ga/wizard/txt/autobuilds.txt'
ICONSETTINGS   = 'http://tvandroidianox.com/Wizard/ajustes.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'darkorange'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][COLOR '+COLOR2+'][/COLOR][/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Version VIPTV Instalada:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME6         = '[COLOR '+COLOR1+']Version VIPTV a instalar:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Gracias por preferir VIPTV Astro\r\n\r\nSi quieres ponerte en contacto escribenos al numero que ves en la tarjeta'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://tvandroidianox.com/Fanart%20Viptv/Logo%20Viptv%202019.png'
CONTACTFANART  = 'http://tvandroidianox.com/Fanart%20Viptv/Tarjeta%20Conctacto%20Alexis%20Viptv.png'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = 'https://stva.zriel.ga/wizard/txt/autobuilds.txt'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.VIPTVAstro'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/AlexisTV/VIPTVAstro/master/addon.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://github.com/AlexisTV/VIPTVAstro/tree/master'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'http://tvandroidianox.com/Wizard2/Viptv%20Notificaciones.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = 'VIPTV ASTRO'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = 'http://tvandroidianox.com/Fanart%20Viptv/Fanart%20de%20Notificaciones.jpg'
#########################################################