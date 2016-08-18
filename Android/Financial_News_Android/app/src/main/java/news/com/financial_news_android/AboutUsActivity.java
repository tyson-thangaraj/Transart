package news.com.financial_news_android;

import android.os.Bundle;
import android.app.Activity;

/**
 * A page showing the description of this app
 *
 * Created by Ping He
 */
public class AboutUsActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // load layout
        setContentView(R.layout.activity_about_us);
    }

}
