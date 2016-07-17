package news.com.financial_news_android;

import android.app.ActionBar;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.v4.widget.DrawerLayout;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.assist.FailReason;
import com.nostra13.universalimageloader.core.listener.ImageLoadingListener;
import com.raizlabs.android.dbflow.config.FlowManager;
import com.raizlabs.android.dbflow.sql.language.Method;
import com.raizlabs.android.dbflow.sql.language.SQLite;
import com.raizlabs.android.dbflow.structure.database.transaction.FastStoreModelTransaction;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import cz.msebera.android.httpclient.Header;

public class FavsActivity extends Activity {

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_favs);

        }
       ListView lv = null;


        @Override
        public void onStart() {
            super.onStart();

            lv =  (ListView) findViewById(R.id.listView);

            lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    Intent i = new Intent(parent.getContext(), NewsActivity.class);
                    i.putExtra("article", articles.get(position));
                    parent.getContext().startActivity(i);
                }
            });


        }

    @Override
    protected void onResume() {
        super.onResume();

        articles = SQLite.select().from(Article.class).where(Article_Table.isFav.is("1")).orderBy(Article_Table.datetime, false).queryList();

        if (articles != null && articles.size() > 0) {
            lv.setAdapter(new UsersAdapter(FavsActivity.this, articles));
        }
    }

    @Override
        public void onStop() {
            super.onStop();


        }



            List<Article> articles = null;


            public class UsersAdapter extends ArrayAdapter<Article> {
                public UsersAdapter(Context context, List<Article> users) {
                    super(context, 0, users);
                }

                @Override
                public View getView(final int position, View convertView, ViewGroup parent) {
                    View v = convertView;

                    if (v == null) {
                        v = LayoutInflater.from(FavsActivity.this).inflate(R.layout.listview_item_main, null);
                    }

                    Article art = getItem(position);
                    ((TextView)v.findViewById(R.id.textView2)).setText(art.getHeadline());
                    String time = art.getDatetime().split("T")[0];
                    ((TextView)v.findViewById(R.id.textView3)).setText(time);

                    final ImageView iv = ((ImageView)v.findViewById(R.id.imageView2));
                    iv.setTag(art);

                    if (art.getImage() != null && !"".equals(art.getImage())) {

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


                    } else {
                        setDefaultPic(iv);
                    }

                    return v;
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
