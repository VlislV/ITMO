package beans;

import Utils.DbManager;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;
import models.Point;

import java.io.Serializable;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.logging.Logger;
@Named("pageManagerBean")
@SessionScoped
public class PageManagerBean implements Serializable {
    private static final Logger logger = Logger.getLogger(PageManagerBean.class.getName());
    private ArrayList<Point> points = new ArrayList<>();

    public ArrayList<Point> getRows(){
        points.clear();
        try(Connection connection = DbManager.getConnection()) {
           Statement st = connection.createStatement();
           st.execute("SELECT * FROM points ORDER BY id DESC");
          ResultSet rs = st.getResultSet();
          while(rs.next()){
              Point point = new Point();
              point.setX(rs.getInt("x"));
              point.setY(rs.getDouble("y"));
              point.setR(rs.getDouble("r"));
              point.setResult(rs.getString("result"));
              point.setStime(rs.getDate("stime"));
              point.setRtime(rs.getDate("rtime"));
              points.add(point);
          }
          return points;
        } catch (SQLException e) {
            logger.info(e.getMessage());
            return points;
        }
    }
}

