package beans;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import java.io.Serializable;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

@Named("mISSProp")
@SessionScoped
public class MISSProp implements MISSPropMBean, Serializable {
    private final AtomicInteger totalMiss = new AtomicInteger();
    private final AtomicInteger totalClicks = new AtomicInteger();

    @Override
    public int getTotalMiss() {
        return totalMiss.get();
    }

    @Override
    public int getTotalClicks() {
        return totalClicks.get();
    }

    @Override
    public double getProp() {
        if(totalClicks.get() == 0){
         return 0.0;
        }
        return (double) totalMiss.get() / totalClicks.get() * 100.0;
    }

    public void updateStats(boolean is_hit){
        totalClicks.incrementAndGet();
        if (!is_hit){
            totalMiss.incrementAndGet();
        }
    }
}
