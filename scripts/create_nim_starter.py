#!/usr/bin/env python3
"""
Create a minimal iOS project template for NIM SDK integration.
Usage: python create_nim_starter.py <project_name> [podfile_content]
"""

import os
import sys
import shutil

def get_latest_nimsdk_lite_version():
    """Get the latest version of NIMSDK_LITE using pod search."""
    import subprocess
    try:
        result = subprocess.run(
            ["pod", "search", "--simple", "NIMSDK_LITE"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'NIMSDK_LITE' in line and 'Latest' in line:
                    import re
                    match = re.search(r'(\d+\.\d+\.\d+)', line)
                    if match:
                        return match.group(1)
    except Exception as e:
        print(f"⚠️ Could not fetch latest NIMSDK_LITE version: {e}")
    return "10.9.75"


def create_project_structure(project_name, podfile_content=None):
    """Create minimal iOS project structure."""

    project_dir = os.path.join(os.getcwd(), project_name)
    xcodeproj_dir = os.path.join(project_dir, f"{project_name}.xcodeproj")
    source_dir = os.path.join(project_dir, project_name)
    base_lproj_dir = os.path.join(source_dir, "Base.lproj")
    assets_dir = os.path.join(source_dir, "Assets.xcassets")

    os.makedirs(xcodeproj_dir, exist_ok=True)
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(base_lproj_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    pbxproj_content = generate_pbxproj(project_name)
    with open(os.path.join(xcodeproj_dir, "project.pbxproj"), "w") as f:
        f.write(pbxproj_content)

    appdelegate_content = """import UIKit
import NECoreKit
import NECoreIM2Kit
import NEChatKit
import NEChatUIKit
import NIMSDK

@main
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // init
        // 设置 IM SDK 的配置项，包括 AppKey，推送配置和一些全局配置等
        let option = NIMSDKOption()
        option.appKey = "your app key"
        option.apnsCername = "网易云信控制台配置的 APNS 推送证书名称"
        option.pkCername = "网易云信控制台配置的 PushKit 推送证书名称"

        // 设置 IM SDK V2 的配置项，包括是否使用旧的登录接口和是否使用云端会话
        let v2Option = V2NIMSDKOption()
        v2Option.enableV2CloudConversation = false

        // 初始化 IM UIKit，初始化 Kit 层和 IM SDK，将配置信息透传给 IM SDK。无需再次初始化 IM SDK
        IMKitClient.instance.setupIM2(option, v2Option)

        return true
    }

    // MARK: UISceneSession Lifecycle
    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }
}
"""
    with open(os.path.join(source_dir, "AppDelegate.swift"), "w") as f:
        f.write(appdelegate_content)

    scenedelegate_content = """import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = ViewController()
        window?.makeKeyAndVisible()
    }
}
"""
    with open(os.path.join(source_dir, "SceneDelegate.swift"), "w") as f:
        f.write(scenedelegate_content)

    viewcontroller_content = """import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white

        // TODO: Add NIM SDK UI integration code here
    }
}
"""
    with open(os.path.join(source_dir, "ViewController.swift"), "w") as f:
        f.write(viewcontroller_content)

    launchscreen_content = """<?xml version="1.0" encoding="UTF-8"?>
<document type="com.apple.InterfaceBuilder3.CocoaTouch.Storyboard.XIB" version="3.0" toolsVersion="21701" targetRuntime="iOS.CocoaTouch" propertyAccessControl="none" useAutolayout="YES" launchScreen="YES" useTraitCollections="YES" useSafeAreas="YES" colorMatched="YES" initialViewController="01J-lp-oVM">
    <device id="retina6_12" orientation="portrait" appearance="light"/>
    <dependencies>
        <plugIn identifier="com.apple.InterfaceBuilder.IBCocoaTouchPlugin" version="21700"/>
        <capability name="Safe area layout guides" minToolsVersion="9.0"/>
        <capability name="documents saved in the Xcode 8 format" minToolsVersion="8.0"/>
    </dependencies>
    <scenes>
        <!--View Controller-->
        <scene sceneID="EHf-IW-A2E">
            <objects>
                <viewController id="01J-lp-oVM" sceneMemberID="viewController">
                    <view key="view" contentMode="scaleToFill" id="Ze5-6b-2t3">
                        <rect key="frame" x="0.0" y="0.0" width="393" height="852"/>
                        <autoresizingMask key="autoresizingMask" widthSizable="YES" heightSizable="YES"/>
                        <viewLayoutGuide key="safeArea" whitekey="Bcu-3y-fUS"/>
                        <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                    </view>
                </viewController>
                <placeholder placeholderIdentifier="IBFirstResponder" id="iYj-Kq-Ea1" userLabel="First Responder" sceneMemberID="firstResponder"/>
            </objects>
            <point key="canvasLocation" x="53" y="375"/>
        </scene>
    </scenes>
    <resources>
        <systemColor name="systemBackgroundColor">
            <color white="1" alpha="1" colorSpace="custom" customColorSpace="genericGamma22GrayColorSpace"/>
        </systemColor>
    </resources>
</document>
"""
    with open(os.path.join(base_lproj_dir, "LaunchScreen.storyboard"), "w") as f:
        f.write(launchscreen_content)

    assets_content = """{
  "info" : {
    "author" : "xcode",
    "version" : 1
  },
  "properties" : {
    "compression-type" : "automatic"
  }
}
"""
    with open(os.path.join(assets_dir, "Contents.json"), "w") as f:
        f.write(assets_content)

    appiconset_dir = os.path.join(assets_dir, "AppIcon.appiconset")
    os.makedirs(appiconset_dir, exist_ok=True)

    appicon_content = """{
  "images" : [
    {
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""
    with open(os.path.join(appiconset_dir, "Contents.json"), "w") as f:
        f.write(appicon_content)

    infoplist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>$(DEVELOPMENT_LANGUAGE)</string>
	<key>CFBundleExecutable</key>
	<string>$(EXECUTABLE_NAME)</string>
	<key>CFBundleIdentifier</key>
	<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>$(PRODUCT_NAME)</string>
	<key>CFBundlePackageType</key>
	<string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0</string>
	<key>CFBundleVersion</key>
	<string>1</string>
	<key>LSRequiresIPhoneOS</key>
	<true/>
	<key>UIApplicationSceneManifest</key>
	<dict>
		<key>UIApplicationSupportsMultipleScenes</key>
		<false/>
		<key>UISceneConfigurations</key>
		<dict>
			<key>UIWindowSceneSessionRoleApplication</key>
			<array>
				<dict>
					<key>UISceneConfigurationName</key>
					<string>Default Configuration</string>
					<key>UISceneDelegateClassName</key>
					<string>$(PRODUCT_MODULE_NAME).SceneDelegate</string>
				</dict>
			</array>
		</dict>
	</dict>
	<key>UILaunchStoryboardName</key>
	<string>LaunchScreen</string>
	<key>UIRequiredDeviceCapabilities</key>
	<array>
		<string>armv7</string>
	</array>
	<key>UISupportedInterfaceOrientations</key>
	<array>
		<string>UIInterfaceOrientationPortrait</string>
		<string>UIInterfaceOrientationLandscapeLeft</string>
		<string>UIInterfaceOrientationLandscapeRight</string>
	</array>
	<key>UISupportedInterfaceOrientations~ipad</key>
	<array>
		<string>UIInterfaceOrientationPortrait</string>
		<string>UIInterfaceOrientationPortraitUpsideDown</string>
		<string>UIInterfaceOrientationLandscapeLeft</string>
		<string>UIInterfaceOrientationLandscapeRight</string>
	</array>
</dict>
</plist>
"""
    with open(os.path.join(source_dir, "Info.plist"), "w") as f:
        f.write(infoplist_content)

    if podfile_content:
        podfile_content = podfile_content.replace("{ProjectName}", project_name)
    else:
        nimsdk_version = get_latest_nimsdk_lite_version()
        podfile_content = f"""# NIM SDK iOS Starter Project Podfile
# Generated by nim-sdk-ios-starter skill
# Latest NIMSDK_LITE version: {nimsdk_version} (run 'pod search --simple NIMSDK_LITE' to check)

platform :ios, '13.0'
use_frameworks!

target '{project_name}' do
  # Option 1: Use NOS_Special subspecs with explicit NIMSDK_LITE version (recommended for custom version)
  pod 'NEChatKit/NOS_Special', '10.9.0'
  pod 'NEChatUIKit/NOS_Special', '10.9.0'
  pod 'NEConversationUIKit/NOS_Special', '10.9.0'
  pod 'NEContactUIKit/NOS_Special', '10.9.0'
  pod 'NETeamUIKit/NOS_Special', '10.9.0'
  pod 'NIMSDK_LITE', '{nimsdk_version}'

  # Option 2: Use base specs without explicit NIMSDK_LITE version (auto-resolved)
  # Uncomment the lines below and comment the lines above if you don't need to specify NIMSDK_LITE version
  # pod 'NEChatKit', '10.9.0'
  # pod 'NEChatUIKit', '10.9.0'
  # pod 'NEConversationUIKit', '10.9.0'
  # pod 'NEContactUIKit', '10.9.0'
  # pod 'NETeamUIKit', '10.9.0'
  # pod 'NIMSDK_LITE'  # Version will be auto-resolved by CocoaPods

  post_install do |installer|
    installer.pods_project.targets.each do |target|
      target.build_configurations.each do |config|
        config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '12.0'
      end
    end
  end
end
"""

    with open(os.path.join(project_dir, "Podfile"), "w") as f:
        f.write(podfile_content)

    readme_content = f"""# {project_name}

A minimal iOS project template for NIM SDK UI integration.

## Requirements

- iOS 13.0+
- Xcode 15.0+
- Swift 5.9+
- CocoaPods

## Getting Started

1. Open the workspace file in Xcode:
   ```bash
   open {project_name}.xcworkspace
   ```

2. Build and run the project

## Project Structure

```
{project_name}/
├── {project_name}.xcodeproj/     # Xcode project
├── {project_name}.xcworkspace/    # CocoaPods workspace (use this!)
├── {project_name}/
│   ├── AppDelegate.swift         # App entry point
│   ├── SceneDelegate.swift       # Scene management (iOS 13+)
│   ├── ViewController.swift      # Main view controller
│   ├── Info.plist                # App configuration with SceneDelegate
│   └── Assets.xcassets/          # App resources (includes AppIcon)
├── Pods/                         # CocoaPods dependencies
└── Podfile                       # Dependency configuration
```

## Simulator Support

**Important:** On Apple Silicon Macs (M1/M2/M3), this project only supports running on **Rosetta simulators (x86_64)**.

- **Simulator**: Requires Rosetta (x86_64) on Apple Silicon Macs - native arm64 simulators are not supported
- **Physical Device**: Fully supported (arm64) - no restrictions

To run on simulator:
1. Select a simulator destination in Xcode
2. Xcode will automatically use Rosetta for arm64 Macs
3. Build and run the project
"""
    with open(os.path.join(project_dir, "README.md"), "w") as f:
        f.write(readme_content)

    return project_dir


def generate_pbxproj(project_name):
    """Generate minimal Xcode project.pbxproj content."""
    return f"""// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{

/* Begin PBXBuildFile section */
		AAAA11111111111111111111 /* AppDelegate.swift in Sources */ = {{isa = PBXBuildFile; fileRef = BBBB22222222222222222222 /* AppDelegate.swift */; }};
		AAAA33333333333333333333 /* SceneDelegate.swift in Sources */ = {{isa = PBXBuildFile; fileRef = BBBB44444444444444444444 /* SceneDelegate.swift */; }};
		AAAA55555555555555555555 /* ViewController.swift in Sources */ = {{isa = PBXBuildFile; fileRef = BBBB66666666666666666666 /* ViewController.swift */; }};
		OOOO00000000000000000001 /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; fileRef = CCCC88888888888888888888 /* Assets.xcassets */; }};
		PPPP11111111111111111111 /* LaunchScreen.storyboard in Resources */ = {{isa = PBXBuildFile; fileRef = CCCC77777777777777777777 /* Base */; }};
/* End PBXBuildFile section */

/* Begin PBXFileReference section */
		BBBB22222222222222222222 /* AppDelegate.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = AppDelegate.swift; sourceTree = "<group>"; }};
		BBBB44444444444444444444 /* SceneDelegate.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = SceneDelegate.swift; sourceTree = "<group>"; }};
		BBBB66666666666666666666 /* ViewController.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ViewController.swift; sourceTree = "<group>"; }};
		BBBB88888888888888888888 /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
		CCCC77777777777777777777 /* Base */ = {{isa = PBXFileReference; lastKnownFileType = file.storyboard; name = Base; path = Base.lproj/LaunchScreen.storyboard; sourceTree = "<group>"; }};
		CCCC88888888888888888888 /* Assets.xcassets */ = {{isa = PBXFileReference; lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = "<group>"; }};
		DDDD99999999999999999999 /* {project_name}.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = {project_name}.app; sourceTree = BUILT_PRODUCTS_DIR; }};
/* End PBXFileReference section */

/* Begin PBXFrameworksBuildPhase section */
		EEEE00000000000000000001 /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXFrameworksBuildPhase section */

/* Begin PBXGroup section */
		FFFF11111111111111111111 = {{
			isa = PBXGroup;
			children = (
				GGGG22222222222222222222 /* {project_name} */,
				HHHH33333333333333333333 /* Products */,
			);
			sourceTree = "<group>";
		}};
		GGGG22222222222222222222 /* {project_name} */ = {{
			isa = PBXGroup;
			children = (
				BBBB22222222222222222222 /* AppDelegate.swift */,
				BBBB44444444444444444444 /* SceneDelegate.swift */,
				BBBB66666666666666666666 /* ViewController.swift */,
				BBBB88888888888888888888 /* Info.plist */,
				CCCC88888888888888888888 /* Assets.xcassets */,
				CCCC77777777777777777777 /* Base */,
			);
			path = {project_name};
			sourceTree = "<group>";
		}};
		HHHH33333333333333333333 /* Products */ = {{
			isa = PBXGroup;
			children = (
				DDDD99999999999999999999 /* {project_name}.app */,
			);
			name = Products;
			sourceTree = "<group>";
		}};
/* End PBXGroup section */

/* Begin PBXNativeTarget section */
		IIII44444444444444444444 /* {project_name} */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = JJJJ55555555555555555555 /* Build configuration list for PBXNativeTarget "{project_name}" */;
			buildPhases = (
				KKKK66666666666666666666 /* Sources */,
				EEEE00000000000000000001 /* Frameworks */,
				LLLL77777777777777777777 /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = {project_name};
			productName = {project_name};
			productReference = DDDD99999999999999999999 /* {project_name}.app */;
			productType = "com.apple.product-type.application";
		}};
/* End PBXNativeTarget section */

/* Begin PBXProject section */
		MMMM88888888888888888888 /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1500;
				LastUpgradeCheck = 1500;
				TargetAttributes = {{
					IIII44444444444444444444 = {{
						CreatedOnToolsVersion = 15.0;
						LastSwiftMigration = 1500;
					}};
				}};
			}};
			buildConfigurationList = NNNN99999999999999999999 /* Build configuration list for PBXProject "MMMM88888888888888888888" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = FFFF11111111111111111111;
			productRefGroup = HHHH33333333333333333333 /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				IIII44444444444444444444 /* {project_name} */,
			);
		}};
/* End PBXProject section */

/* Begin PBXResourcesBuildPhase section */
		LLLL77777777777777777777 /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				OOOO00000000000000000001 /* Assets.xcassets in Resources */,
				PPPP11111111111111111111 /* LaunchScreen.storyboard in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXResourcesBuildPhase section */

/* Begin PBXSourcesBuildPhase section */
		KKKK66666666666666666666 /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				AAAA55555555555555555555 /* ViewController.swift in Sources */,
				AAAA33333333333333333333 /* SceneDelegate.swift in Sources */,
				AAAA11111111111111111111 /* AppDelegate.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
/* End PBXSourcesBuildPhase section */

/* Begin PBXVariantGroup section */
		CCCC77777777777777777777 /* Base */ = {{
			isa = PBXVariantGroup;
			children = (
				CCCC77777777777777777777 /* Base */,
			);
			name = Base;
			sourceTree = "<group>";
		}};
/* End PBXVariantGroup section */

/* Begin XCBuildConfiguration section */
		QQQQ22222222222222222222 /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				INFOPLIST_FILE = "{project_name}/Info.plist";
				INFOPLIST_KEY_CFBundleDisplayName = "{project_name}";
				INFOPLIST_KEY_LSApplicationCategoryType = "public.app-category.utilities";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = 13.0;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "com.example.{project_name}";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SDKROOT = iphoneos;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
				"EXCLUDED_ARCHS[sdk=iphonesimulator*]" = "arm64";
			}};
			name = Debug;
		}};
		RRRR33333333333333333333 /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES;
				CLANG_ANALYZER_NONNULL = YES;
				CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE;
				CLANG_CXX_LANGUAGE_STANDARD = "gnu++20";
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CLANG_ENABLE_OBJC_WEAK = YES;
				CLANG_WARN_BLOCK_CAPTURE_AUTORELEASING = YES;
				CLANG_WARN_BOOL_CONVERSION = YES;
				CLANG_WARN_COMMA = YES;
				CLANG_WARN_CONSTANT_CONVERSION = YES;
				CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS = YES;
				CLANG_WARN_DIRECT_OBJC_ISA_USAGE = YES_ERROR;
				CLANG_WARN_DOCUMENTATION_COMMENTS = YES;
				CLANG_WARN_EMPTY_BODY = YES;
				CLANG_WARN_ENUM_CONVERSION = YES;
				CLANG_WARN_INFINITE_RECURSION = YES;
				CLANG_WARN_INT_CONVERSION = YES;
				CLANG_WARN_NON_LITERAL_NULL_CONVERSION = YES;
				CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF = YES;
				CLANG_WARN_OBJC_LITERAL_CONVERSION = YES;
				CLANG_WARN_OBJC_ROOT_CLASS = YES_ERROR;
				CLANG_WARN_QUOTED_INCLUDE_IN_FRAMEWORK_HEADER = YES;
				CLANG_WARN_RANGE_LOOP_ANALYSIS = YES;
				CLANG_WARN_STRICT_PROTOTYPES = YES;
				CLANG_WARN_SUSPICIOUS_MOVE = YES;
				CLANG_WARN_UNGUARDED_AVAILABILITY = YES_AGGRESSIVE;
				CLANG_WARN_UNREACHABLE_CODE = YES;
				CLANG_WARN__DUPLICATE_METHOD_MATCH = YES;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_NO_COMMON_BLOCKS = YES;
				GCC_WARN_64_TO_32_BIT_CONVERSION = YES;
				GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR;
				GCC_WARN_UNDECLARED_SELECTOR = YES;
				GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE;
				GCC_WARN_UNUSED_FUNCTION = YES;
				GCC_WARN_UNUSED_VARIABLE = YES;
				INFOPLIST_FILE = "{project_name}/Info.plist";
				INFOPLIST_KEY_CFBundleDisplayName = "{project_name}";
				INFOPLIST_KEY_LSApplicationCategoryType = "public.app-category.utilities";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				IPHONEOS_DEPLOYMENT_TARGET = 13.0;
				LOCALIZATION_PREFERS_STRING_CATALOGS = YES;
				MTL_ENABLE_DEBUG_INFO = NO;
				MTL_FAST_MATH = YES;
				SDKROOT = iphoneos;
				SUPPORTED_PLATFORMS = "iphoneos iphonesimulator";
				SWIFT_COMPILATION_MODE = wholemodule;
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};
		SSSS44444444444444444444 /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = NO;
				INFOPLIST_FILE = "{project_name}/Info.plist";
				INFOPLIST_KEY_CFBundleDisplayName = "{project_name}";
				INFOPLIST_KEY_LSApplicationCategoryType = "public.app-category.utilities";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "com.example.{project_name}";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Debug;
		}};
		TTTT55555555555555555555 /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon;
				ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor;
				CODE_SIGN_STYLE = Automatic;
				CURRENT_PROJECT_VERSION = 1;
				ENABLE_PREVIEWS = YES;
				GENERATE_INFOPLIST_FILE = NO;
				INFOPLIST_FILE = "{project_name}/Info.plist";
				INFOPLIST_KEY_CFBundleDisplayName = "{project_name}";
				INFOPLIST_KEY_LSApplicationCategoryType = "public.app-category.utilities";
				INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES;
				INFOPLIST_KEY_UIApplicationSupportsIndirectInputEvents = YES;
				INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen;
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad = "UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone = "UIInterfaceOrientationPortrait UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight";
				LD_RUNPATH_SEARCH_PATHS = (
					"$(inherited)",
					"@executable_path/Frameworks",
				);
				MARKETING_VERSION = 1.0;
				PRODUCT_BUNDLE_IDENTIFIER = "com.example.{project_name}";
				PRODUCT_NAME = "$(TARGET_NAME)";
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Release;
		}};
/* End XCBuildConfiguration section */

/* Begin XCConfigurationList section */
		JJJJ55555555555555555555 /* Build configuration list for PBXNativeTarget "{project_name}" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				SSSS44444444444444444444 /* Debug */,
				TTTT55555555555555555555 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		NNNN99999999999999999999 /* Build configuration list for PBXProject "MMMM88888888888888888888" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				QQQQ22222222222222222222 /* Debug */,
				RRRR33333333333333333333 /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
/* End XCConfigurationList section */
	}};
	rootObject = MMMM88888888888888888888 /* Project object */;
}}
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_nim_starter.py <project_name> [podfile_content]")
        sys.exit(1)

    project_name = sys.argv[1]
    podfile_content = sys.argv[2] if len(sys.argv) > 2 else None

    project_dir = create_project_structure(project_name, podfile_content)
    print(f"✅ Project created: {project_dir}")

    import subprocess
    print("📦 Running pod install...")
    result = subprocess.run(["pod", "install"], cwd=project_dir, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Pod install completed successfully!")
        print(f"📱 Open the project with: open {project_name}.xcworkspace")
    else:
        print("⚠️ Pod install encountered issues:")
        print(result.stderr)
        print(f"📦 Try running manually: cd {project_name} && pod install")


if __name__ == "__main__":
    main()
