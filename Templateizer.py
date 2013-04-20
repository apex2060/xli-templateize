import sublime, sublime_plugin, re, datetime

now = datetime.datetime.now()

class TemplateizeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s=self.view.substr(sublime.Region(0, self.view.size()))
		region = sublime.Region(0, self.view.size())
		self.view.erase(edit, region)

		s=s.replace('\\', '\\\\')
		s=s.replace('\'', '\\\'')
		s=s.replace('\"', '\\\"')
		s=s.replace('<', '\u003c')
		s=s.replace('>', '\u003e')
		s=s.replace('\n', '\\n')

		o='\n/****************************** NEW TEMPLATE ******************************/';
		o+='\n/********** \tCOMPILED ON: \t'+str(now)+' \t\t **********/';
		o+='\nnewTemplate = \''+s+'\';';
		o+='\n/****************************** END TEMPLATE ******************************/';
		self.view.insert(edit, self.view.size(), o)



class DeTemplateizeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s=self.view.substr(sublime.Region(0, self.view.size()))
		region = sublime.Region(0, self.view.size())
		self.view.erase(edit, region)

		s=s.replace('\\n', '\n')
		s=s.replace('\u003e', '>')
		s=s.replace('\u003c', '<')
		s=s.replace('\\\"', '\"')
		s=s.replace('\\\'', '\'')
		s=s.replace('\\\\', '\\')

		o='\n/****************************** OLD TEMPLATE ******************************/';
		o+='\n/********** \tDE-COMPILED ON: \t'+str(now)+' \t **********/';
		o+='\n'+s;
		o+='\n/***************************** OLD TEMPLATE ******************************/';
		o+='\n/********* NOTE: Remove comments before compiling as a template. *********/';
		self.view.insert(edit, self.view.size(), o)

class ExtractMoreCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s=self.view.substr(sublime.Region(0, self.view.size()))
		arr = s.split('<%')

		region = sublime.Region(0, self.view.size())
		self.view.erase(edit, region)

		j=''
		h=''
		ct=0
		for p1 in arr:
			arr2 = p1.split('%>')
			if len(arr2) == 2:
				j+=arr2[0]
				j+='[#'+str(ct)+'#]'
				h+=arr2[1]
				h+='[#'+str(ct)+'#]'
			else:
				h+='[#'+str(ct)+'#]'
				j+=arr2[0]
				j+='[#'+str(ct)+'#]'
			ct+=1

		h=h.replace("   <", "\n>");
		h=h.replace("  <", "\n>");
		h=h.replace(" <", "\n<");
		h=h.replace("<", "\n<");

		r='\n/**********HTML**********/\n'
		r+=h
		r+='\n/**********JS**********/\n'
		r+=j
		self.view.insert(edit, self.view.size(), r)

class ReCombineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s=self.view.substr(sublime.Region(0, self.view.size()))
		s=s.replace("\n<", "<");
		arr = s.split('/**********HTML**********/')
		arr = arr[1].split('/**********JS**********/');
		html = arr[0].split('[#');
		js = arr[1].split('[#');

		region = sublime.Region(0, self.view.size())
		self.view.erase(edit, region)

		xHtml=[]
		for h in html:
			xHtml.append( h.split('#]') );
		xJs=[]
		for j in js:
			xJs.append( j.split('#]') );


		o=''
		for x in range(0, len(xHtml)):
			h=xHtml[x]
			if len(h) == 2:
				j=xJs[int(h[0])+1]
				if len(j) == 2:
					o+='<%'+j[1]+'%>'+h[1]
				else:
					o+=h[1]
		self.view.insert(edit, self.view.size(), o)