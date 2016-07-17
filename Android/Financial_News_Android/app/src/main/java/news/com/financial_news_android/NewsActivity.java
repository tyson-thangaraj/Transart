package news.com.financial_news_android;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.util.Base64;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.assist.FailReason;
import com.nostra13.universalimageloader.core.listener.ImageLoadingListener;
import com.raizlabs.android.dbflow.config.FlowManager;
import com.raizlabs.android.dbflow.sql.language.SQLite;
import com.raizlabs.android.dbflow.structure.database.transaction.FastStoreModelTransaction;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;

import cz.msebera.android.httpclient.Header;

public class NewsActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_news);

        final Article art = getIntent().getParcelableExtra("article");
        Article temp = SQLite.select(Article_Table.isFav).from(Article.class).where(Article_Table.articleid.is(art.getArticleid())).querySingle();

        art.setIsFav(temp.getIsFav());
        ((TextView) findViewById(R.id.textView8)).setText(art.getHeadline());
        ((TextView) findViewById(R.id.textView9)).setText(art.getContent());

        final ImageView fav = (ImageView) findViewById(R.id.imageView9);
        fav.setImageResource("1".equals(art.getIsFav()) ? R.drawable.favourite_select : R.drawable.favourite_news);
        fav.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if ("1".equals(art.getIsFav())) {
                    SQLite.update(Article.class).set(Article_Table.isFav.eq("0"))
                            .where(Article_Table.articleid.is(art.getArticleid())).execute();
                    //Article temp = SQLite.select(Article_Table.isFav).from(Article.class).where(Article_Table.articleid.is(art.getArticleid())).querySingle();
                    fav.setImageResource(R.drawable.favourite_news);
                    art.setIsFav("0");
                } else {
                    SQLite.update(Article.class).set(Article_Table.isFav.eq("1"))
                            .where(Article_Table.articleid.is(art.getArticleid())).execute();
                    //Article temp = SQLite.select(Article_Table.isFav).from(Article.class).where(Article_Table.articleid.is(art.getArticleid())).querySingle();
                    fav.setImageResource(R.drawable.favourite_select);
                    art.setIsFav("1");
                }
            }
        });

        final Handler h = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);

                ArrayList<Match> matches = (ArrayList<Match>) msg.obj;

                int size = matches.size();
                findViewById(R.id.relatedstory).setVisibility(size==0?View.GONE:View.VISIBLE);
                for (int i = 0; i < size; i++) {
                    Article temp = SQLite.select().from(Article.class).where(Article_Table.articleid.is(matches.get(i).getMatchid())).querySingle();
                    View view=null;
                    if (i == 0) {
                        findViewById(R.id.r1).setVisibility(View.VISIBLE);
                        setRelated(temp,view);
                    } else if (i == 1) {
                        findViewById(R.id.r2).setVisibility(View.VISIBLE);
                        setRelated(temp,view);
                    } else if (i == 2) {
                        findViewById(R.id.r3).setVisibility(View.VISIBLE);
                        setRelated(temp,view);
                    } else if (i == 3) {
                        findViewById(R.id.r4).setVisibility(View.VISIBLE);
                        setRelated(temp,view);
                    } else if (i == 4) {
                        findViewById(R.id.r5).setVisibility(View.VISIBLE);
                        setRelated(temp,view);
                    }
                }

            }
        };

        //findViewById(R.id.relatedstory).setVisibility("BBC".equals(art.getSource()) ? View.VISIBLE : View.GONE);

        if ("BBC".equals(art.getSource())) {
            AsyncHttpClient c = new AsyncHttpClient();

            RequestParams rp = new RequestParams();
            rp.add("format", "json");
            rp.add("selectedArticleID", String.valueOf(art.getArticleid()));
            rp.add("limit", String.valueOf(5));

            c.get("http://137.43.93.133:8000/articlematch/matchlist/", rp, new JsonHttpResponseHandler() {
                @Override
                public void onSuccess(int statusCode, Header[] headers, JSONArray response) {
                    super.onSuccess(statusCode, headers, response);

                    int size = response.length();
                    ArrayList<Match> matches = new ArrayList<Match>();
                    JSONObject obj;
                    Match match;
                    for (int i = 0; i < size; i++) {
                        match = new Match();

                        try {
                            obj = response.getJSONObject(i);
                            match.setArticleid(Long.parseLong(obj.getString("News")));
                            match.setMatchid(Long.parseLong(obj.getString("Match_News")));
                            match.setWeight(Long.parseLong(obj.getString("Weight")));

                            matches.add(match);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                    if(matches.size()>0)
                    {
                    FastStoreModelTransaction.insertBuilder(FlowManager.getModelAdapter(Match.class))
                            .addAll(matches).build().execute(FlowManager.getDatabase(AppDatabase.class).getWritableDatabase());

                    h.sendMessage(Message.obtain(h, 1, matches));}

                }


                @Override
                public void onFailure(int statusCode, Header[] headers, String responseString, Throwable throwable) {
                    super.onFailure(statusCode, headers, responseString, throwable);
                }
            });
        } else {
            findViewById(R.id.relatedstory).setVisibility(View.GONE);
        }

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



    public void setRelated(Article art,View v){
    ((TextView)v.findViewById(R.id.textView2)).

    setText(art.getHeadline()

    );
    String time = art.getDatetime().split("T")[0];
    ((TextView)v.findViewById(R.id.textView3)).

    setText(time);

    final ImageView iv = ((ImageView) v.findViewById(R.id.imageView2));
    iv.setTag(art);

    if(art.getImage()!=null&&!"".

    equals(art.getImage()

    ))

    {

        File file = imageExsit(Base64.encodeToString(art.getImage().getBytes(), Base64.DEFAULT) + ".jpg");
        //ImageLoader.getInstance().displayImage(Uri.fromFile(file).toString(), iv);
        if (file != null)
            try {
                //iv.setImageBitmap(BitmapFactory.decodeStream(new FileInputStream(file)));
                String u = Uri.fromFile(file).toString();
                ImageLoader.getInstance().displayImage(Uri.decode(u), iv);
            } catch (Exception e) {
                setDefaultPic(iv);
            }
        else {
            setDefaultPic(iv);

            //Bitmap b = ImageLoader.getInstance().loadImageSync(art.getImage());
            ImageLoader.getInstance().displayImage(art.getImage(), iv, new ImageLoadingListener() {
                @Override
                public void onLoadingStarted(String imageUri, View view) {

                }

                @Override
                public void onLoadingFailed(String imageUri, View view, FailReason failReason) {

                }

                @Override
                public void onLoadingComplete(String imageUri, View view, Bitmap loadedImage) {
                    saveImage(loadedImage,
                            Base64.encodeToString(imageUri.getBytes(), Base64.DEFAULT) + ".jpg");
                }

                @Override
                public void onLoadingCancelled(String imageUri, View view) {

                }
            });
        }

        Intent i = new Intent(this, NewsActivity.class);
        i.putExtra("article", art);
        this.startActivity(i);


    }

    else

    {
        setDefaultPic(iv);
    }
}

    public void setDefaultPic(ImageView iv) {
        Article art = (Article) iv.getTag();
        String source = art.getSource();

        if ("The New York Times".equals(art.getSource())) {
            iv.setImageResource(R.drawable.nytime);
        }else if ("BBC".equals(art.getSource())) {
            iv.setImageResource(R.drawable.bbc);
        }else if ("ChinaDaily".equals(art.getSource())) {
            iv.setImageResource(R.drawable.chinadaily);
        }else if ("Reuters".equals(art.getSource())) {
            iv.setImageResource(R.drawable.reuters);
        }else {
            iv.setImageResource(R.drawable.sample);
        }


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

    public String saveImage(Bitmap finalBitmap, String fname) {

        String root = Environment.getExternalStorageDirectory().toString();
        File myDir = new File(root + "/financial_eye");
        if (!myDir.exists()) {
            myDir.mkdirs();
        }

        File file = new File(myDir, fname);
        if (file.exists())
            return file.getAbsolutePath();

        try {
            FileOutputStream out = new FileOutputStream(file);
            finalBitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
            out.flush();
            out.close();

        } catch (Exception e) {
            return "";
        }

        return file.getAbsolutePath();
    }

}
