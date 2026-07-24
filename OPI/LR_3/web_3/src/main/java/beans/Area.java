package beans;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import java.io.Serializable;
import java.util.concurrent.atomic.AtomicReference;

@Named("area")
@SessionScoped
public class Area implements AreaMBean, Serializable {
    private final AtomicReference<Double> area = new AtomicReference<>(0.0);
    @Override
    public double getArea() {
        return area.get();
    }

    @Override
    public void calculateArea(double r) {
        area.set(r * (r / 2) + r * (r / 2) / 2 + 3.14 * r * r / 4);
    }
}