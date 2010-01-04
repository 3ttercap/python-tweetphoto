#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# pythonTweetPhoto - Dead-simple TweetPhoto image uploader.

# Copyright (c) 2009, Marcel Caraciolo
# caraciol@gmail.com
# twitter: marcelcaraciolo

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

__author__ = 'caraciol@gmail.com'
__version__ = '0.1'

import httplib, mimetypes
from urllib import urlopen
from xml.dom import minidom as xml

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO



class TweetPhotoAPI(object):
	SERVER = 'tweetphotoapi.com'
	UPLOAD_URL = '/api/tpapi.svc/upload2'

	
	def __init__(self,username,password,apikey,image=None,filename=None,
					server=SERVER,upload_url = UPLOAD_URL):
		"""Initializer of the TweetPhotoAPI, object that holds the TweetPhoto
			username/password/apiKey and server information. 
			Parameters:
				username: twitter username
				password: twitter password
				apikey: The TweetPhoto API Key. It can be acquired at http://tweetphoto.com/developer
				image: The path to the image
				server: the SERVER url
				upload_url: the upload url
			"""
		
		self.server = server
		self.username = username
		self.password = password
		self.apiKey = apikey
		self.filename = filename
		self.filedata = None
		self.image = image
		self.upload_url = upload_url
		self.connection = httplib.HTTP(self.server)
							

	def upload(self,image=None, message=None, tags=None, geoLocation=None,post_to_twitter = False):
		""" Method called to upload a photo to TweetPhoto Web Service
			Parameters:
				image: the Image Path
				message: the message for the photo, limited to 200 characters.
				tags: a comma delimited list of tags for the photo (e.g. 'cat,awesome,funny')'
				geoLocation: a string in the format lat,long with the geolocation tag for latitude and longitude
				post_to_twitter:  Whether or not to post to twitter.
			Return:
			 	If uploaded: the url media  else: the error code
		"""
		
		BLOCKSIZE = 8192
		
		if image:
			self.image = image
		self.get_filedata()
				
		
		body_txt = self.filedata.getvalue()
			
		self.connection.putrequest('POST', '/%s' %self.upload_url)
		self.connection.putheader('content-type','application/x-www-form-urlencoded')
		self.connection.putheader('TPAPIKEY', self.apiKey)
		self.connection.putheader('TPAPI', self.username + ',' + self.password)
		self.connection.putheader('TPMIMETYPE', self.get_content_type())
		
		if post_to_twitter: #Default value is False
			self.connection.putheader('TPPOST', 'True')
			
		if message is not None: #Default value is Null
			self.connection.putheader('TPMSG', message)
		
		if tags is not None: #Default value is Null
			self.connection.putheader('TPTAGS',tags)
		
		if geoLocation is not None: #Default value is Null
			g = geoLocation.split(',')
			self.connection.putheader('TPLAT',g[0])
			self.connection.putheader('TPLONG', g[1])
		
		self.connection.putheader('content-length', str(len(body_txt)))
		self.connection.endheaders()
		
		offs = 0
		for i in range(0, len(body_txt), BLOCKSIZE):
			offs += BLOCKSIZE
			self.connection.send(body_txt[i:offs])
		
		
		statusCode, statusMsg, headers = self.connection.getreply()
		if statusCode != 201:
			raise Exception('Error uploading image: TweetPhoto returned HTTP \
							  %s (%s)' % (statusCode,statusMsg))
		
		response = self.connection.file.read()
				
		return self.parse_xml(response)
		
	def get_filedata(self):
		""" Method to get the image content in bytes
		"""
		if self.filename is None:
			try:
				import Image
			except ImportError:
				self.filedata = StringIO.StringIO(urlopen(self.image).read())
			else:
				self.filedata = StringIO.StringIO(urlopen(self.image).read())
				img = Image.open(self.filedata)
		else:
			try:
				self.filedata = StringIO.StringIO(self.image)
			except Exception, e:
				print e
			self.image = self.filename
		

	def get_content_type(self):
		"""Get the image content type"""
		return mimetypes.guess_type(self.image)[0] or 'application/octet-stream'

	
	def parse_xml(self, xml_response):
		""" Method to parse the WebService response (xml data)
			Return:
				the media url or the error code
		"""
 		dom = xml.parseString(xml_response)
		node = dom.getElementsByTagName('Status')
		if str(node[0].childNodes[0].data) == 'OK':
			#return URL
			url = dom.getElementsByTagName('MediaUrl')
			return url[0].childNodes[0].data
		elif str(node[0].childNodes[0].data) == 'fail':
			errorNode = dom.getElementsByTagName('ErrorCode')
			if str(errorNode[0].childNodes[0].data) == '1001':
				#Invalid twitter username or password
				return 1001
			elif str(errorNode[0].childNodes[0].data) == '1002':
				#Image not found
				return 1002
			elif str(errorNode[0].childNodes[0].data) == '1003':
				#Invalid Image type
				return 1003
			elif str(errorNode[0].childNodes[0].data) == '1004':
				#Imager larger than 5 MB
				return 1004
			elif str(errorNode[0].childNodes[0].data) == '1005':
				#Image location not found
				return 1005
			elif str(errorNode[0].childNodes[0].data) == '1006':
				#Not valid extension
				return 1006
			elif str(errorNode[0].childNodes[0].data) == '1009':
				#Invalid API Key or key no longe in use
				return 1009
		
		#Unidentified error
		return 0
	
	
	
		
if __name__ == '__main__':
	from optparse import OptionParser
	optPsr = OptionParser('usage: %prog -u USER_NAME -p PASSWORD -k API_KEY [options] IMG_PATH')
	optPsr.add_option('-u', '--user', type='string', help='TweetPhoto user name')
	optPsr.add_option('-p', '--passwd', type='string', help='TweetPhoto password')
	optPsr.add_option('-k', '--key' , type='string', help= 'TweetPhoto API key')
	optPsr.add_option('-b', '--both' , action='store_true', default=False, 
					help = 'post to twitter together')
	optPsr.add_option('-m', '--msg', type='string' , help = 'message, if multiple words put inside quotes')
	optPsr.add_option('-t', '--tags', type='string' , help = 'tags must be separated by comma like: cats,animals')
	optPsr.add_option('-l', '--geo' , type='string', help = 'GeoLocation (Must be separated by commas like: -14.00,-15.00)')

	(opts,args) = optPsr.parse_args()
	
	if not opts.user:
		optPsr.error('no USER_NAME')
		
	if not opts.passwd:
		optPsr.error('no PASSWORD')
	
	if not opts.key:
		optPsr.error('no API_KEY')
		
	if not args:
		optPsr.error('no IMG_PATH to upload')
		
	if opts.geo:
		geoPosition = opts.geo.split(',')
		if len(geoPosition) == 2:
			try:
				geoPosition = (float(geoPosition[0]),float(geoPosition[1]))
			except:
				optPsr.error('Invalid format of GeoLocation. It must be: lat,long')
		else:
			optPsr.error('Invalid format of GeoLocation. It must be: lat,long')
			
		
	if len(args) > 1:
		optPsr.error('multiple img upload not allowed')
		
		
	tweetPhoto = TweetPhotoAPI(opts.user, opts.passwd, opts.key)
	
	posted_url = tweetPhoto.upload(args[0], message=opts.msg, tags=opts.tags, 
					geoLocation = opts.geo, post_to_twitter = opts.both)
	
	print posted_url