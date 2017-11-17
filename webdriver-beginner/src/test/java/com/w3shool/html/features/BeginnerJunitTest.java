package com.w3shool.html.features;

import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class BeginnerJunitTest{

	@Test
	public void testOpenBrowser() {

		System.setProperty("webdriver.chrome.driver", ".\\drivers\\chromedriver.exe");

		WebDriver driver = new ChromeDriver();
		driver.get("http://demoqa.com/");
		
		
		driver.quit();

	}

}