package com.asksqa.steps;

import com.asksqa.pages.LoginScreen;

import net.thucydides.core.annotations.Step;
import net.thucydides.core.steps.ScenarioSteps;

public class LoginSteps extends ScenarioSteps {

	private static final long serialVersionUID = 1L;

	private LoginScreen onLoginScreen;

	@Step
	public LoginBuilder connectApp() {
		return new LoginBuilder(onLoginScreen);
	}

	public static class LoginBuilder {

		private LoginScreen onLoginScreen;

		public LoginBuilder(LoginScreen onLoginScreen) {
			this.onLoginScreen = onLoginScreen;
			this.onLoginScreen.clickOnSettingIcon();
		}

		public LoginBuilder withHost(String host) {
			onLoginScreen.enterIntoHost(host);
			return this;
		}

		public LoginBuilder withPort(String port) {
			onLoginScreen.enterIntoPort(port);
			onLoginScreen.clickOnDoneBtn();
			return this;

		}

		public LoginBuilder withUserName(String username) {
			onLoginScreen.enterIntoUserName(username);
			return this;
		}

		public LoginBuilder withPassword(String pwd) {
			onLoginScreen.enterIntoPassword(pwd);
			return this;
		}
		
		public LoginBuilder withCompany(String company) {
			onLoginScreen.selectCompany(company);
			return this;
		}

		public void process() {
			onLoginScreen.clickOnLoginButton();
		}

	}

}
