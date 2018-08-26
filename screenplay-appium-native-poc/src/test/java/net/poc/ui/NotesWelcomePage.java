package net.poc.ui;

import org.openqa.selenium.By;

import io.appium.java_client.MobileBy;
import net.serenitybdd.screenplay.targets.Target;

public class NotesWelcomePage {

    public static final Target ADD_NOTE_BUTTON =
            Target.the("Add a note button").located(By.id("com.example.android.testing.notes:id/fab_add_notes"));
    public static final Target NOTES = Target.the("Notes ").located(
            MobileBy.AndroidUIAutomator("new UiSelector().className(\"android.widget.FrameLayout\").clickable(true)"));
    public static final String TITLE_NOTE_SELECTOR = "new UiSelector().resourceId(\"com.example.android.testing.notes:id/note_detail_title\")";
    public static final String DESCRIPTION_NOTE_SELECTOR = "new UiSelector().resourceId(\"com.example.android.testing.notes:id/note_detail_description\")";

}
