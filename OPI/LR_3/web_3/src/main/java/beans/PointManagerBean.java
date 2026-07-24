package beans;

import Utils.Checker;
import Utils.DbManager;
import Utils.MBeanMan;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;

import java.io.Serializable;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

@Named("pointManagerBean")
@SessionScoped
public class PointManagerBean implements Serializable {
    private static final Logger logger = Logger.getLogger(PointManagerBean.class.getName());
    private static final ResourceBundle messages =
            ResourceBundle.getBundle("locales");

    Checker checker = new Checker();
    @Inject
    private MBeanMan mBeanMan;
    private final Hit hit = new Hit();
    private final Area area = new Area();

    @PostConstruct
    public void init() {
        String sessionId = getSessionId();
        mBeanMan.registerBean(hit, "Hit_" + sessionId);
        mBeanMan.registerBean(area, "Area_" + sessionId);
        logger.info("MBeans registered for session: " + sessionId);
    }

    @PreDestroy
    public void destroy() {
        mBeanMan.unregisterBean(area);
        mBeanMan.unregisterBean(hit);
        logger.info("MBeans unregistered");
    }

    private String getSessionId() {
        FacesContext context = FacesContext.getCurrentInstance();
        if (context != null && context.getExternalContext().getSession(false) != null) {
            return String.valueOf(context.getExternalContext().getSession(false).hashCode());
        }
        return String.valueOf(System.currentTimeMillis());
    }


    public void savePoint(PointBean pointBean) {
        String sql = "INSERT INTO points (x, y, r, result, stime, rtime) VALUES (?, ?, ?, ?, ?, ?)";

        try (Connection connection = DbManager.getConnection();
             PreparedStatement pstmt = connection.prepareStatement(sql)) {

            pstmt.setInt(1, pointBean.getX());
            pstmt.setDouble(2, pointBean.getY());
            pstmt.setDouble(3, pointBean.getR());
            pstmt.setString(4, pointBean.getResult());

            Timestamp currentTime = new Timestamp(System.currentTimeMillis());
            pstmt.setTimestamp(5, currentTime);
            pstmt.setTimestamp(6, currentTime);

            int rowsAffected = pstmt.executeUpdate();
            logger.info(messages.getString("db.save.success") + rowsAffected);
            boolean isHit = !("MISS".equalsIgnoreCase(pointBean.getResult()));
            hit.updateStats(isHit, pointBean.getX(), pointBean.getY(), pointBean.getR());
            area.calculateArea(pointBean.getR());

        } catch (SQLException e) {
            logger.log(Level.SEVERE, messages.getString("db.save.error"), e);
            throw new RuntimeException(messages.getString("db.save.failed"), e);
        }
    }

    public void throwPoint(PointBean pointBean) {
        try {
            logger.info(pointBean.getX().toString() +
                    pointBean.getY().toString() +
                    pointBean.getR().toString());
            pointBean.setResult(checker.check(pointBean));
            savePoint(pointBean);
        } catch (Exception e) {
            logger.log(Level.WARNING, e.getMessage());
            FacesContext context = FacesContext.getCurrentInstance();
            context.addMessage(null,
                    new FacesMessage(FacesMessage.SEVERITY_ERROR,
                            messages.getString("error.title"),
                            e.getMessage()));
        }
    }
}