package news.com.financial_news_android;

import android.os.Parcel;
import android.os.Parcelable;

import com.raizlabs.android.dbflow.annotation.Column;
import com.raizlabs.android.dbflow.annotation.PrimaryKey;
import com.raizlabs.android.dbflow.annotation.Table;
import com.raizlabs.android.dbflow.structure.BaseModel;

/**
 * A model corresponding to table Match
 *
 * Created by Ping He
 */
@Table(database = AppDatabase.class)
public class Match extends BaseModel{

    @PrimaryKey(autoincrement = true)
    long id;

    // the article id of the news
    @Column
    private long articleid;

    // the article id of the matched news
    @Column
    private long matchid;

    // similarity between the two news
    @Column
    private double weight;

    public long getArticleid() {
        return articleid;
    }

    public void setArticleid(long articleid) {
        this.articleid = articleid;
    }

    public long getMatchid() {
        return matchid;
    }

    public void setMatchid(long matchid) {
        this.matchid = matchid;
    }

    public double getWeight() {
        return weight;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

}
