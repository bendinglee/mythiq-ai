from branches.plugin_api_store.preset_installer import install_preset
from branches.plugin_api_store.store_browser import list_store_plugins

def test_plugin_api():
    store = list_store_plugins()
    assert len(store) > 0, "❌ Store missing plugin packs"

    result = install_preset("starter_creative")
    assert result["success"], "❌ Plugin pack install failed"

    print("✅ Plugin API test passed.")

if __name__ == "__main__":
    test_plugin_api()
