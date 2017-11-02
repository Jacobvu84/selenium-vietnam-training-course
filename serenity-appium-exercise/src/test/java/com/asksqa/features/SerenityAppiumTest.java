package com.asksqa.features;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.WebDriver;

import com.asksqa.steps.LoginSteps;

import net.serenitybdd.junit.runners.SerenityRunner;
import net.thucydides.core.annotations.Managed;
import net.thucydides.core.annotations.Manual;
import net.thucydides.core.annotations.Steps;

@RunWith(SerenityRunner.class)
public class SerenityAppiumTest {

	@Managed(driver = "appium")
	WebDriver driver;

	@Steps
	LoginSteps loginStep;
	
	@Test
	@Manual
	public void showManualTestOnReport(){}

	@Test
	public void connectAppToDatabase() {
		
		loginStep.connectApp()
		         .withHost("xxx.xxx.xxx.xxx")
		         .withPort("xxxx")
		         .withUserName("vuthelinh")
		         .withPassword("missyousomuch")
		         .withCompany("Ask SQA Pte Ltd")
		         .process();
	}

}
