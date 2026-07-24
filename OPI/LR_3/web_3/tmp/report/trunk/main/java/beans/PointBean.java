package beans;

import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Named;
import models.Point;

import java.io.Serializable;
import java.util.Date;

@Named("pointBean")
@RequestScoped
public class PointBean implements Serializable {
    private Integer x = -2;
    private Double y = -3.0;
    private Double r = 2.0;
    private String result;
    private Date stime, rtime;

    public Date getRtime() {
        return rtime;
    }

    public void setRtime(Date rtime) {
        this.rtime = rtime;
    }

    public Integer getX() {
        return x;
    }

    public void setX(Integer x) {
        this.x = x;
    }
    
    public PointBean() {}


    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public Double getR() {
        return r;
    }

    public void setR(Double r) {
        this.r = r;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public Date getStime() {
        return stime;
    }

    public void setStime(Date stime) {
        this.stime = stime;
    }
    public void clear(){
        this.x = -2;
        this.y = -3.0;
        this.r = 2.0;
    }
    public void wrap(Point point){
        this.x = point.getX();
        this.y = point.getY();
        this.r = point.getR();
        this.result = point.getResult();
        this.stime = point.getStime();
        this.rtime = point.getRtime();
    }
}
