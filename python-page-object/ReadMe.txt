	This is sample web automation test project with new structure that based on Page Object pattern and it also is popular test automation framework

	The overall project structure is shown below: 3 modules / layers
		+ pages (webium)
    			PageObjects: All common method will be defined here (wrapper selenium API to share)
				xxx_page: Find the WebElements of that web page and also contains Page methods which perform operations on those WebElements.
		+ steps
    			Tasks and assertions performed by the "user"
		+ features
			Test Scripts


https://github.com/wgnet/webium

pip install future  (>=0.14)
pip install waiting (>=1.2.1)