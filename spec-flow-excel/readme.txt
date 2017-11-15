
SpecFlow+ Excel  (SpecFlow Plugin)
==================================

This SpecFlow plugin enables writing SpecFlow tests in Excel files. You can 
specify SpecFlow feature files in Excel or extend scenario outlines in normal 
feature files with further examples from Excel.

The package also contains a converter too that can be used to convert Excel 
files to Gherkin and vica versa.

Please check our website (http://www.specflow.org/plus/Excel) for an 
introduction and a getting started guide. 

Please also check the documentation pages at 
http://www.specflow.org/plus/documentation.

The feature files describing the possibilites with the plugin can be found in 
the 'docs' folder of this package.

Contact
^^^^^^^

Please send your feedback to info@specflowplus.com.

Licensing
^^^^^^^^^

The component can be purchased as part of 
SpecFlow+. See http://www.specflow.org/plus/ for details.

Evaluation: You can evaluate all features of SpecFlow+ Excel for free. 
In evaluation mode, an extra scenario is generated with title 
"SpecFlow+ Excel Evaluation Mode". Please purchase at 
http://www.specflow.org/plus/ to remove this limitation.
See http://www.specflow.org/plus/Evaluation for details.

Important notes
^^^^^^^^^^^^^^^

This package enables the build-time generation feature of SpecFlow by adding an 
MsBuild target to the project file. This ensures that the tests from the Excel 
files are re-generated when necessary.

How to add a new Excel feature file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Converting Between Gherkin and Excel
You can use the SpecFlow+ Excel converter command line tool to convert Excel files to Gherkin syntax and vice versa.

1. To convert an Excel file to Gherkin:
SpecFlow.Plus.Excel.Converter.exe convert EXCEL_FILE_PATH TARGET_FILE_PATH

2. To convert a Gherkin file to Excel:
SpecFlow.Plus.Excel.Converter.exe initialize FEATURE_FILE_PATH TARGET_FILE_PATH
More information can be found 

http://www.specflow.org/plus/documentation/SpecFlowPlus-Excel-Command-Line-Tool-Reference/