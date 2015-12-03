"""This module creates a comic viewer window, which allows one to view the
online webcomic Sandra and Woo."""
import pygtk
pygtk.require('2.0')
import gtk
import urllib2
from lxml import html

class MainWin(object):
	"""This class creates the main window of the program."""

	def destroy(self, widget, data=None):
		"""Handle when the window is closed."""
		gtk.main_quit()

	def __init__(self):
		"""Create the main window."""
		self.cur_comic = 0
		self.image_urls = get_img_urls()

		# Create the main window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		self.window.set_size_request(1200, 900)

		# Create the table to store the window elements
		self.table = gtk.Table(2, 2, True)
		self.table.show()

		# Create the buttons
		self.button_up = gtk.Button(label="Next")
		self.button_up.connect("button-press-event", self.button_up_press)
		self.button_up.show()
		self.button_down = gtk.Button(label="Back")
		self.button_down.connect("button-press-event", self.button_down_press)
		self.button_down.show()

		# Create the scrollbox to contain the image
		self.scroll_box = gtk.ScrolledWindow()
		self.scroll_box.set_border_width(10)
		self.scroll_box.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scroll_box.show()

		# Add the section for the comic image
		self.image = gtk.Image()
		self.image.show()

		# Add items to the table and window
		self.window.add(self.table)
		self.scroll_box.add_with_viewport(self.image)
		self.table.attach(self.scroll_box, 0, 2, 0, 1)
		self.table.attach(self.button_up, 0, 1, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
		self.table.attach(self.button_down, 1, 2, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)

		# Show the window
		self.window.show()
		self.update_comic()

	def update_comic(self):
		"""Update the comic shown in the window."""
		url = self.image_urls[self.cur_comic]
		hdr = { \
			'User-Agent':'Mozilla/5.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
		}
		req = urllib2.Request(url, headers=hdr)
		response = urllib2.urlopen(req)
		loader = gtk.gdk.PixbufLoader()
		loader.write(response.read())
		loader.close()
		self.image.set_from_pixbuf(loader.get_pixbuf())

	def comic_up(self):
		"""Move to the next comic."""
		if self.cur_comic < (len(self.image_urls) - 1):
			self.cur_comic = self.cur_comic + 1
			self.update_comic()
	def comic_down(self):
		"""Return to the previous comic."""
		if self.cur_comic > 0:
			self.cur_comic = self.cur_comic - 1
			self.update_comic()

	def button_up_press(self, object, arg1):
		"""Handle when the next comic button is pressed."""
		self.comic_up()

	def button_down_press(self, object, arg1):
		"""Handle when the back comic button is pressed."""
		self.comic_down()

	def main(self):
		gtk.main()

def get_img_urls():
	"""Get a list of all of the urls of the images of the comic."""
	# Setup the url and header request to get the html from the archive page
	url = "http://www.sandraandwoo.com/archive/"
	hdr = { \
		'User-Agent':'Mozilla/5.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
	}

	# Retrive the html of the archive page
	req = urllib2.Request(url, headers=hdr)
	response = urllib2.urlopen(req)
	tree = html.fromstring(response.read())

	# Get all of the links from the archive page
	links = tree.xpath('//a[@rel="bookmark"]/@href')

	# Change the list to be decending and remove the first element as it is not relevent
	links.reverse()
	links = links[1:]

	# Create a list of all of the comic image urls
	img_links = []
	for item in links:
		end = ".png"
		if item[39:43] == "fana" or item[39:43] == "0050":
			end = ".jpg"
		if item[39:43] == "woo/":
			item = item[:-1] + "!"  + item[-1:]

		if item[39].isdigit() and item[39:43] != "5-ye" and int(item[39:43]) < 243:
			item = item[0:28] + "comics/" + item[28:32] + "-" + item[33:35] + "-" + item[36:38] + "-" + \
				"[" + item[39:43] + "]" + item[43:-1] + end
		else:
			item = item[0:28] + "comics/" + item[28:32] + "-" + item[33:35] + "-" + item[36:38] + "-" + \
				item[39:-1] + end

		img_links.append(item)

	# Return the list of comic image urls
	return img_links

def main():
	"""Start the program and create the main window."""
	MainWin().main()
	return 0

if __name__ == "__main__":
	main()
