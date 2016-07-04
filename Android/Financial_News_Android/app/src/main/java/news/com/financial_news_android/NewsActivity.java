package news.com.financial_news_android;

import android.app.Activity;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Base64;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.assist.FailReason;
import com.nostra13.universalimageloader.core.listener.ImageLoadingListener;

import org.w3c.dom.Text;

import java.io.File;

public class NewsActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_news);

        Article art = getIntent().getParcelableExtra("article");
        ((TextView)findViewById(R.id.textView8)).setText(art.getHeadline());
        ((TextView)findViewById(R.id.textView9)).setText(art.getContent());

        ImageView iv = (ImageView) findViewById(R.id.imageView10);
        if (art.getImage() != null && !"".equals(art.getImage())) {

            File file = imageExsit(Base64.encodeToString(art.getImage().getBytes(), Base64.DEFAULT) + ".jpg");
            //ImageLoader.getInstance().displayImage(Uri.fromFile(file).toString(), iv);
            if (file != null)
                try {
                    //iv.setImageBitmap(BitmapFactory.decodeStream(new FileInputStream(file)));
                    String u = Uri.fromFile(file).toString();
                    ImageLoader.getInstance().displayImage(Uri.decode(u), iv);
                } catch (Exception e) {
                    iv.setVisibility(View.GONE);
                }
            else {
                iv.setVisibility(View.GONE);
            }


        } else {
            iv.setVisibility(View.GONE);
        }


        findViewById(R.id.imageView8).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }

    public File imageExsit(String fname) {
        String root = Environment.getExternalStorageDirectory().toString();
        File myDir = new File(root + "/financial_eye");
        if (!myDir.exists()) {
            myDir.mkdirs();
        }

        File file = new File(myDir, fname);
        if (file.exists()) {
            if (file.length() == 0) {
                file.delete();
                return null;
            }
            return file;
        }

        return null;
    }
}
