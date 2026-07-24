package beans;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import javax.management.*;
import java.io.Serializable;
import java.util.concurrent.atomic.AtomicInteger;

@Named("hitArea")
@SessionScoped
public class HitArea implements HitAreaMBean, NotificationBroadcaster, Serializable {

    private final AtomicInteger totalThrows = new AtomicInteger();
    private final AtomicInteger totalHits = new AtomicInteger();
    private final AtomicInteger consecMisses = new AtomicInteger();

    private final NotificationBroadcasterSupport broadcaster = new NotificationBroadcasterSupport();
    @Override
    public int getThrows() {
        return totalThrows.get();
    }


    @Override
    public int getHits() {
        return totalHits.get();
    }

    @Override
    public void checkForConsecMisses() {
        if(consecMisses.get() == 4){
            broadcaster.sendNotification(new Notification(
                    "consec.misses",
                    this,
                    System.currentTimeMillis(),
                    "4 consec misses!!!"
            ));
            consecMisses.set(0);
        }
    }


    public void updateStats(boolean is_hit){
        totalThrows.incrementAndGet();
        if (is_hit){
            totalHits.incrementAndGet();
            consecMisses.set(0);
        }else{
            consecMisses.incrementAndGet();
        }
        checkForConsecMisses();
    }


    @Override
    public void addNotificationListener(NotificationListener listener, NotificationFilter filter, Object handback) throws IllegalArgumentException {
        broadcaster.addNotificationListener(listener, filter, handback);
    }

    @Override
    public void removeNotificationListener(NotificationListener listener) throws ListenerNotFoundException {
        broadcaster.removeNotificationListener(listener);
    }

    @Override
    public MBeanNotificationInfo[] getNotificationInfo() {
        String[] types = new String[] {"consec.misses"};
        String name = Notification.class.getName();
        String description = "Notify when 4 consec misses are recorded";
        return new MBeanNotificationInfo[] {new MBeanNotificationInfo(
                types, name, description
        )};
    }
}
