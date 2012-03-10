import datetime

color = 'blue'

def gen_header():
    '''Creates the html header'''
    
    htmlfile = open('index.html','w')
    lastupdate = datetime.date.today()
    
    
    
    header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
                   <title>Arch Sheriff</title>
                   <link rel="stylesheet" href="webpage/sheriff.css" type="text/css" />
                   <script type="text/javascript" src="webpage/jquery-1.2.6.js"></script> 
                   <script type="text/javascript" src="webpage/jquery.tablesorter.js"></script> 
                   <script type="text/javascript" id="js">
                               $(document).ready(function() 
                              { 

	                              $("#VULNERABILITIES").tablesorter({
		                               widgets: ['zebra'], widgetZebra: {css: ["","blue"]} });

                                      $("#WARNINGS").tablesorter({
		                               widgets: ['zebra'], widgetZebra: {css: ["","blue"]} });  
    
                                      $("#End Of Life").tablesorter({
                                               widgets: ['zebra'], widgetZebra: {css: ["","blue"]} });  
                               } 
                               ); 
                      </script>
    </head>
    
    <body>
    <div id="head_container">
	    <div id="title">		
			<div id="logo">		
				    <h1 id="archtitle">
						<a href="/" title="Arch Linux (Home)">Arch Linux</a>
				    </h1>		
			</div>
	    </div>

	    <div id="main_nav">	    
		<ul>
		    <li><a href="#End Of Life">EOL</a></li>		    
                    <li><a href="#WARNINGS">Warnings</a></li>                    
                    <li><a href="#VULNERABILITIES">Vulnerabilities</a></li>		    
		    <li><a href="http://code.google.com/p/arch-sheriff/">Project Page</a></li>	    
		    <li class="selected"><a href="/">Home</a></li>
		</ul>	    
	    </div>           
            
            <div id="brdmenu" class="inbox">
            Last update: ''' + lastupdate.isoformat() + '''
            </div>      
            
     </div>
     
   <h1><span class="title1">Arch</span><span class="title2">Sheriff</span></h1>
   <h2>A script to match NetBSD vulnerability database against Arch Linux packages</h2>'''
    
    
    htmlfile.write(header)
    htmlfile.close()

def gen_table(title, position, total):
    
    htmlfile = open('index.html','a')
    
    if position == 'begin':    
        
        table = '<h3>' + title + ' (' + str(total) + ''')</h3>
        <table id="''' + title + '''">
        <thead>
        <tr class="header">
        <th>Package</th>
        <th>Arch Version</th>
        <th>Version Affected</th>
        <th>Vuln Type</th>
        </tr>
        </thead>
        <tbody>\n'''
    
    if position == 'end':
        table = '''</tbody>
       </table>\n'''    
    
    htmlfile.write(table)
    htmlfile.close()
    
def gen_tableline(content):

    htmlfile = open('index.html','a')
    line = htmlfile.write('<tr><th>' + content[0] + '</th><th>' + content[1] + '</th><th>' + content[2] + '</th><th><a href="' + content[4]+ '">' + content[3] + '</a></th></tr>\n')    
    
    htmlfile.close()
    
def gen_footer():
    htmlfile = open('index.html','a')
    html = '''
    <div id="footer">
    Arch Sheriff is a work in progress, for issues and feature requests please contact us at: 
    <a href="http://code.google.com/p/arch-sheriff/">http://code.google.com/p/arch-sheriff/</a>
    </div>
    </body>
    </html>'''
    
    htmlfile.write(html)
    htmlfile.close()