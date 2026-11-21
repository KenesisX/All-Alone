// OPTIONAL BUT RECOMMENDED — grant WebRTC (camera/mic) inside the WebView.
// After `npx cap add android`, edit:
//   android/app/src/main/java/tech/strikeback/allalone/MainActivity.java
// and replace its body with this. It auto-grants the in-page getUserMedia
// permission prompt (the Android *runtime* permission is still requested
// normally via the manifest below).

package tech.strikeback.allalone;

import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    this.bridge.getWebView().setWebChromeClient(new WebChromeClient() {
      @Override
      public void onPermissionRequest(final PermissionRequest request) {
        runOnUiThread(() -> request.grant(request.getResources()));
      }
    });
  }
}
