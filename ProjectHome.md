A simple python library to upload photos to the [TweetPhoto](http://tweetphoto.com/) WebService using its API.  It's also possible to upload photos to [Twitter](http://twitter.com) using the TweetPhoto API.

Added the [PyS60](https://garage.maemo.org/projects/pys60) library for Symbian S60 Phones support (s60tweetphoto.py)

**Version 0.2: Added support to JSON protocol + new advanced functions**

**Version 0.1: Initial Release**


To upload a photo (if you're a developer) it's necessary to request an API key to TweetPhoto WebService. See how here:  [TweetPhoto Developer Program](http://tweetphoto.com/developer)

# Usage #

To install the PyTweetPhoto, you can download the .zip file at the download section.

You can install it by doing the command at your console/terminal:

` python setup.py install `


To use the PyS60 library, you have to import it to your application source code.

Here some examples, see below.

```

>>> import pyTweetPhoto
>>> api = pyTweetPhoto.TweetPhotoAPI('USERNAME','PASSWORD','APIKEY')
>>> posted_url = api.upload('FILE_LOCATION')
>>> #Post to Twitter
>>> #posted_url = api.upload('FILE_LOCATION',post_to_twitter=True)
>>> #posted_url = api.upload('FILE_LOCATION',message='Photo uploaded!', tags='web,photo,python',
...       #                      geoLocation='-9.0,12.0' , post_to_twitter=True)
>>> print posted_url


>>>#ONLY AVAILABLE FOR PC VERSION!
>>>#you can get pictures details
>>>details =api.GetPhotoDetails(photo_id= 94114845)
>>>print details

>>>#You can add/remove comments
>>>response = api.AddComment(photo_id= 94141845, message='THis is a comment!')
>>>response = api.RemoveComment(photo_id=94148145,comment_id=203430)

>>>#You can Add/Remove Favorites (including Posting to twitter)
>>>response = api.FavoritePhoto(photo_id= 94148415,post_to_twitter=True)
>>>response = api.RemoveFavoritePhoto(photo_id= 94148145)

>>>#You can Vote (like or dislike vote ThumbsUp/Down)
>>>response = api.VoteThumbsUp(photo_id= 94148415)
>>>response = api.VoteThumbsDown(photo_id= 94148415)


>>>#You can check in (flag that user says that he has seen the photo) the photo.
>>>response = api.CheckInPhoto(photo_id= 94148451)


>>>#You can Delete the photo (if he has uploaded it).
>>response = api.DeletePhoto(photo_id= 94148451)

```


# Usage via Commandline #

To use the command line you have to download the tweetPhotoUp.py that can be found in the folder demo inside the package.
To use it, you have to put the PyTweetPhoto.py at the same folder or install the PyTweetPhoto.py


```
 $python tweetPhotoUp.py -h

Usage: tweetPhotoUp.py -u USER_NAME -p PASSWORD -k API_KEY [options] IMG_PATH

Options:
  -h, --help            show this help message and exit
  -u USER, --user=USER  TweetPhoto user name
  -p PASSWD, --passwd=PASSWD
                        TweetPhoto password
  -k KEY, --key=KEY     TweetPhoto API key
  -b, --both            post to twitter together
  -m MSG, --msg=MSG     message, if multiple words put inside quotes
  -t TAGS, --tags=TAGS  tags must be separated by comma like: cats,animals
  -l GEO, --geo=GEO     GeoLocation (Must be separated by commas like:
                        -14.00,-15.00)
```