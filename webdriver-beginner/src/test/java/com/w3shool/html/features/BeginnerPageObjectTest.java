package com.w3shool.html.features;

import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

import net.serenitybdd.core.pages.PageObject;
import net.thucydides.core.annotations.DefaultUrl;

@DefaultUrl("http://demoqa.com/")
public class BeginnerPageObjectTest extends PageObject {

	@Test
	public void testOpenBrowser() {

		System.setProperty("webdriver.chrome.driver", ".\\drivers\\chromedriver.exe");

		WebDriver driver = new ChromeDriver();
		setDriver(driver);
		open();

		element("//a[text()='Registration']").click();
		
		
		getDriver().quit();

	}

}