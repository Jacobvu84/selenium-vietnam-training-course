package serenitybdd.appiumtest.features;


import static net.serenitybdd.screenplay.GivenWhenThen.givenThat;
import static net.serenitybdd.screenplay.GivenWhenThen.when;
import static net.serenitybdd.screenplay.GivenWhenThen.seeThat;
import static net.serenitybdd.screenplay.GivenWhenThen.then;
import static org.hamcrest.Matchers.hasItem;
import static org.hamcrest.Matchers.is;

import static net.serenitybdd.screenplay.actors.OnStage.theActorCalled;
import static net.serenitybdd.screenplay.actors.OnStage.theActorInTheSpotlight;

import java.io.IOException;
import java.net.MalformedURLException;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.WebDriver;

import io.appium.java_client.service.local.AppiumDriverLocalService;
import net.poc.model.Note;
import net.poc.questions.factory.NoteDashboard;
import net.poc.tasks.AddANote;
import net.serenitybdd.junit.runners.SerenityRunner;
import net.serenitybdd.screenplay.Actor;
import net.serenitybdd.screenplay.abilities.BrowseTheWeb;
import net.serenitybdd.screenplay.actors.OnStage;
import net.serenitybdd.screenplay.actors.OnlineCast;
import net.thucydides.core.annotations.Managed;

@RunWith(SerenityRunner.class)
public class WhenUsingAHybridAppStory {
	
    @Managed(driver = "Appium")
    public WebDriver hisMobileDevice;

    //Actor anna = Actor.named("Anna");
    String jacob = "Jacob Vu";
    static AppiumDriverLocalService appiumService = null;


    
    private Note note = new Note();

    @BeforeClass
    public static void startAppiumServer() throws IOException {
        appiumService = AppiumDriverLocalService.buildDefaultService();
        appiumService.start();
    }

    @Before
    public void annaCanBrowseTheMobileApp() throws MalformedURLException {
       // givenThat(anna.can(BrowseTheWeb.with(herMobileDevice)));
    	OnStage.setTheStage(new OnlineCast());
        
    }

    @AfterClass
    public static void stopAppiumServer() {
        appiumService.stop();
    }

    @Test
    public void add_a_note_with_title_and_description() {
       
        this.note = new Note.NoteBuilder().called("Test Note").
                withDescription("Description Test").build();
        
        theActorCalled(jacob).can(BrowseTheWeb.with(hisMobileDevice));
        
        theActorInTheSpotlight().attemptsTo(AddANote.with(note));
        
        theActorInTheSpotlight().should(
            seeThat(NoteDashboard.numberOfNotes(),is(3)),
            seeThat(NoteDashboard.displayed(), hasItem(note))
        );
        
        //givenThat(anna).wasAbleTo(AddANote.with(note));

       // when(anna).attemptsTo(AddANote.with(note));

        //then(anna).should(seeThat(NoteDashboard.numberOfNotes(),is(3)),
        //		          seeThat(NoteDashboard.displayed(), hasItem(note)));
    }




}