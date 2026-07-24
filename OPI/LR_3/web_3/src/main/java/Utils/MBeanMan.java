package Utils;


import jakarta.enterprise.context.ApplicationScoped;
import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

import javax.management.*;
import java.lang.management.ManagementFactory;
import java.util.HashMap;
import java.util.Map;

@WebListener
@ApplicationScoped
public class MBeanMan implements ServletContextListener {
    private final Map<Class<?>, ObjectName> beans = new HashMap<>();

    public void registerBean(Object bean, String name) {
        try {
            var domain = bean.getClass().getPackageName();
            var type = bean.getClass().getSimpleName();
            var objectName = new ObjectName(
                    String.format("%s:type=%s,name=%s", domain, type, name)
            );

            ManagementFactory.getPlatformMBeanServer().registerMBean(bean, objectName);
            beans.put(bean.getClass(), objectName);
        } catch (InstanceAlreadyExistsException | MBeanRegistrationException
                 | NotCompliantMBeanException | MalformedObjectNameException ex) {
            ex.printStackTrace();
        }
    }

    public void unregisterBean(Object bean) {
        if (!beans.containsKey(bean.getClass())) {
            throw new IllegalArgumentException("Specified bean is not registered.");
        }

        try {
            ManagementFactory.getPlatformMBeanServer()
                    .unregisterMBean(beans.get(bean.getClass()));
            beans.remove(bean.getClass());
        } catch (InstanceNotFoundException | MBeanRegistrationException ex) {
            ex.printStackTrace();
        }
    }

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        System.out.println("MBeanMan initialized");
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        for (Class<?> beanClass : beans.keySet()) {
            try {
                ManagementFactory.getPlatformMBeanServer()
                        .unregisterMBean(beans.get(beanClass));
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        beans.clear();
        System.out.println("MBeanMan destroyed");
    }
}