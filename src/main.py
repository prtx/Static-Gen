#!/usr/bin/python3

import argparse, os, yaml, markdown, jinja2
from utils import get_log

def parse_args(args=None):
	
	"""
	Parse command line arguments.
	"""

	parser = argparse.ArgumentParser(description="A simple python based static generator.")
	parser.add_argument("--init", action="store_true", help="Initialize project.")

	if args:
		return parser.parse_args(args)
	return parser.parse_args()


def initialize():

	"""
	Initialize static-gen environment.
	"""
	
	config = {
		'project_name': input("Project Name: "),
		'site_title': input("Site Title: "),
		'author': input("Author/s: "),
		'asset_directory': "assets",
		'template_directory': "templates",
		'static_directory': "static",
		'cms_directory': "cms",
		'logfile': "log.txt",
		'template': input("Default template(index.html): ") or "index.html",
	}
	
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

	config = yaml.load(open("config.yml"))

	def __init__(self):
				
		for root, dirs, files in os.walk(self.config['cms_directory']):
			
			project_config = self.config
			
			current_directory = os.path.join(root, ".")
			directory_config = project_config
			if os.path.isfile(current_directory+"/config.yml"):
				directory_config.update(yaml.load(open(self.current_directory+"/config.yml").read()))

			for dir in dirs:
				os.system("mkdir -p "+os.path.join(self.config['static_directory'], dir))
			
			contents = []
			for file_name in files:
				file_name, extension = os.path.splitext(file_name)
				file_path = os.path.join(root, file_name).lstrip(self.config['cms_directory']).rstrip(file_name)
				
				if extension == '.md':
					file_config = directory_config
					if os.path.isfile(os.path.join(root, file_name+".yml")):
						file_config.update(yaml.load(open(os.path.join(root, file_name+".yml")).read()))
					content = self.get_content(file_name)
					contents.append(content)
					self.generate_static(file_name, file_path, content, file_config)
			
			dir = current_directory.split("/")[-2]
			if dir!=self.config['cms_directory']:
				self.generate_static(dir.lower(), file_path, "\n\n".join(contents), directory_config)
	
	
	def get_content(self, file_name):
		return markdown.markdown(open(os.path.join(self.config['cms_directory'], file_name+".md")).read())
	
	def generate_static(self, file_name, file_path, content, config):
		
		config['content'] = content
		config['static'] = "." + "/.."*(file_path.count("/")-1)
		template = open(self.config['template_directory']+"/"+config["template"]).read()
		html = jinja2.Template(template).render(config)
		page = open(self.config['static_directory']+file_path+file_name+".html", "w")
		page.write(html)

if __name__=="__main__":
	args = parse_args()
	'''if args.init:
		initialize()'''
	StaticGen()
