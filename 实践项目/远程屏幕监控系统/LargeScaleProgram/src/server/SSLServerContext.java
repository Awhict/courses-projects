package server;

import javax.net.ssl.*;
import java.io.FileInputStream;
import java.security.KeyStore;

public class SSLServerContext {

    private static final String KEYSTORE_PATH = "SERVER\\serverkeystore.jks";
    private static final String KEYSTORE_PASSWORD = "password";
    private static final String TRUSTSTORE_PATH = "SERVER\\servertruststore.jks";
    private static final String TRUSTSTORE_PASSWORD = "password";

    public static SSLContext getSSLContext() throws Exception {
        // Load server keystore
        KeyStore serverKeyStore = KeyStore.getInstance("JKS");
        serverKeyStore.load(new FileInputStream(KEYSTORE_PATH), KEYSTORE_PASSWORD.toCharArray());

        // Load server truststore
        KeyStore trustStore = KeyStore.getInstance("JKS");
        trustStore.load(new FileInputStream(TRUSTSTORE_PATH), TRUSTSTORE_PASSWORD.toCharArray());

        // Initialize key manager factory
        KeyManagerFactory keyManagerFactory = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        keyManagerFactory.init(serverKeyStore, KEYSTORE_PASSWORD.toCharArray());

        // Initialize trust manager factory
        TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        trustManagerFactory.init(trustStore);

        // Create SSL context
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(keyManagerFactory.getKeyManagers(), trustManagerFactory.getTrustManagers(), null);

        return sslContext;
    }
}
