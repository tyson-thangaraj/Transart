package news.com.financial_news_android;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import org.w3c.dom.Text;

public class NewsActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_news);

        Article art = getIntent().getParcelableExtra("article");
        ((TextView)findViewById(R.id.textView8)).setText(art.getHeadline());
        ((TextView)findViewById(R.id.textView9)).setText(art.getContent());

        findViewById(R.id.imageView8).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}
