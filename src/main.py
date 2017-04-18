#!/usr/bin/python3

import argparse, os, yaml, markdown, jinja2, datetime
from utils import get_log
from copy import deepcopy


def parse_args(args=None):
	
	"""
	Parse command line arguments.
	"""

	parser = argparse.ArgumentParser(description="A simple python based static generator.")
	parser.add_argument("--init", action="store_true", help="Initialize project.")

	if args:
		return parser.parse_args(args)
	return parser.parse_args()


def generate_config():
	
	return {
		'project_name': input("Project Name: "),
		'site_title': input("Site Title: "),
		'author': input("Author/s: "),
		'asset_directory': "assets",
		'template_directory': "templates",
		'static_directory': "static",
		'cms_directory': "cms",
		'logfile': "log.txt",
		'template': input("Default template(index.html): ") or "index.html",
		'list)template': input("Default list template: ") or "index.html",
	}


def initialize():

	"""
	Initialize static-gen environment.
	"""
	
	config = generate_config()
	
	os.system("mkdir -p "+config['project_name'])
	os.system("cd "+config['project_name'])
	
	log = get_log(config['project_name']+"/"+config['logfile'])

	with open(config['project_name']+"/config.yml", "w") as config_file:
		yaml.dump(config, config_file, default_flow_style=False)
	log.info("Created config file")
	
	os.system("mkdir -p "+config['project_name']+"/"+config['asset_directory'])
	log.info("Created asset directory")
	os.system("mkdir -p "+config['project_name']+"/"+config['template_directory'])
	log.info("Created template directory")
	os.system("mkdir -p "+config['project_name']+"/"+config['static_directory'])
	log.info("Created static directory")
	os.system("mkdir -p "+config['project_name']+"/"+config['cms_directory'])
	log.info("Created cms directory")
	


class StaticGen:
	
	def __init__(self):
		self.config = yaml.load(open("config.yml"))
		self.log = get_log(self.config['logfile'])

	def run(self):
				
		for root, dirs, files in os.walk(self.config['cms_directory']):
			
			project_config = deepcopy(self.config)
			
			current_directory = os.path.join(root, ".")
			directory_config = deepcopy(project_config)
			directory_config = self.update_config(directory_config, current_directory+"/config.yml")

			for dir in dirs:
				os.system("mkdir -p "+os.path.join(self.config['static_directory'], dir))
			
			contents = []
			files.sort(key=lambda file: os.path.getmtime(os.path.join(root, file)))
			for file_name in self.arrange_files(files):
				file_name, extension = os.path.splitext(file_name)
				file_path = os.path.join(root, file_name).lstrip(self.config['cms_directory']).rstrip(file_name)
				
				if extension == '.md':
					file_config = deepcopy(directory_config)
					file_config = self.update_config(file_config, os.path.join(root, file_name+".yml"))
					content, info = self.get_data(file_path+file_name)
					contents.append(info)
					
					file_config['content'] = markdown.markdown(content)
					file_config['static'] = "." + "/.."*(file_path.count("/")-1)
					self.generate_static(file_name, file_path, file_config)
			
			dir = current_directory.split("/")[-2]
			if dir!=self.config['cms_directory']:

				directory_config['content_list'] = contents
				directory_config['static'] = "." + "/.."*(file_path.count("/")-1)
				directory_config['template'] = directory_config['list_template']

				self.generate_static(dir.lower(), file_path, directory_config)
	
	def update_config(self, config, config_file):
		
		if os.path.isfile(config_file):
			self.log.info("Updating config with "+config_file)
			config.update(yaml.load(open(config_file).read()))

		return config
	
	def arrange_files(self, files):

		return files[::-1]


	def get_data(self, file_name):
		
		self.log.info("Reading content from "+file_name+".md")
		cms_file = self.config['cms_directory']+file_name+".md"
		content = open(cms_file).read()
		time = os.path.getmtime(cms_file)
		info = {
			'content': markdown.markdown("\n".join(content.split("\n")[:5])+"..."),
			'link': file_name+".html",
			'time': datetime.datetime.fromtimestamp(time).strftime("%d %b %Y")
		}

		return content, info
	

	def generate_static(self, file_name, file_path, config):
		
		self.log.info("Generating static page "+file_path+file_name+".html with template "+config['template'])
		
		environment = jinja2.environment.Environment()
		environment.loader = jinja2.FileSystemLoader(self.config['template_directory'])
		template = environment.get_template(config["template"])
		html = template.render(config)
		page = open(self.config['static_directory']+file_path+file_name+".html", "w")
		page.write(html)

if __name__=="__main__":
	args = parse_args()
	#if args.init:
	#initialize()
	a = StaticGen()
	a.run()
