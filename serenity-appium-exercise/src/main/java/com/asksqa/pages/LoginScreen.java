package com.asksqa.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import com.asksqa.MobilePageObject;

import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSFindBy;
import net.serenitybdd.core.annotations.findby.By;

public class LoginScreen extends MobilePageObject {

	public LoginScreen(WebDriver driver) {
		super(driver);
	}

	final static String groupIdApp = "synergix.android:id/";

	@AndroidFindBy(id = groupIdApp + "settingMenuItem")
	@iOSFindBy(xpath = "")
	private WebElement settingIcon;

	@AndroidFindBy(id = groupIdApp + "host")
	private WebElement hostField;

	@AndroidFindBy(id = groupIdApp + "port")
	private WebElement portField;

	@AndroidFindBy(id = groupIdApp + "masterSettingConfirmButton")
	private WebElement submitBtn;

	@AndroidFindBy(id = groupIdApp + "textUserName")
	private WebElement usrnameField;

	@AndroidFindBy(id = groupIdApp + "textPassword")
	private WebElement pwdField;

	@AndroidFindBy(id = groupIdApp + "mainDb")
	private WebElement mainDbField;

	@AndroidFindBy(id = "android:id/text1")
	private WebElement firstCompany;

	@AndroidFindBy(id = groupIdApp + "btnLogin")
	private WebElement loginBtn;

	public void clickOnSettingIcon() {
		settingIcon.click();
	}

	public void enterIntoHost(String host) {

		hostField.clear();
		hostField.sendKeys(host);
	}

	public void enterIntoPort(String port) {
		portField.clear();
		portField.sendKeys(port);
	}

	public void clickOnDoneBtn() {
		submitBtn.click();
	}

	public void enterIntoUserName(String username) {
		usrnameField.sendKeys(username);
	}

	public void enterIntoPassword(String pwd) {
		pwdField.sendKeys(pwd);
	}

	public void selectCompany(String company) {
		mainDbField.click();
		chooseCompany(company).click();
		getDriver().navigate().back();

	}

	private WebElement chooseCompany(String company) {
		return getDriver().findElement(By.xpath("//android.widget.CheckedTextView[@text='" + company + "']"));
	}

	public void clickOnLoginButton() {
		loginBtn.click();
	}

}
