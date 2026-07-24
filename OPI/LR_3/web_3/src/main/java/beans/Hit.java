package beans;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import javax.management.*;
import java.io.Serializable;
import java.util.concurrent.atomic.AtomicInteger;

@Named("hit")
@SessionScoped
public class Hit implements HitMBean, NotificationBroadcaster, Serializable {

    private final AtomicInteger totalPoints = new AtomicInteger();
    private final AtomicInteger totalHits = new AtomicInteger();

    private final NotificationBroadcasterSupport broadcaster = new NotificationBroadcasterSupport();

    private static final double box_sz = 300;

    @Override
    public int getTotalPoints() {
        return totalPoints.get();
    }

    @Override
    public int getHits() {
        return totalHits.get();
    }

    @Override
    public void checkPointOutOfBounds(int x, double y, double r) {
        if(x / r * 100 + 150 < 0 || x / r * 100 + 150 > box_sz || -(y / r * 100 - 150) < 0 || -(y / r * 100 - 150) > box_sz){
            broadcaster.sendNotification(new Notification("point.out.of.bounds",
                    this, System.currentTimeMillis(),
                    "Point was thrown out of box"));
        }
    }

    public void updateStats(boolean isHit, int x, double y, double r) {
        checkPointOutOfBounds(x, y, r);
        totalPoints.incrementAndGet();
        if (isHit) {
            totalHits.incrementAndGet();
        }
    }

    @Override
    public void addNotificationListener(NotificationListener listener, NotificationFilter filter, Object handback) {
        broadcaster.addNotificationListener(listener, filter, handback);
    }

    @Override
    public void removeNotificationListener(NotificationListener listener) throws ListenerNotFoundException {
        broadcaster.removeNotificationListener(listener);
    }

    @Override
    public MBeanNotificationInfo[] getNotificationInfo() {
        String[] types = new String[] {"point.out.of.bounds"};
        String name = Notification.class.getName();
        String description = "Notify when point is outside area";
        return new MBeanNotificationInfo[] {
                new MBeanNotificationInfo(types, name, description)
        };
    }
}