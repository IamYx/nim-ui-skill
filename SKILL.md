---
name: nim-sdk-ios-starter
description: 生成空的 iOS 项目示例用于指导用户接入带 UI 界面的 NIM SDK，包含 Podfile 模板和 pod install 执行。Use when user wants to create a minimal iOS project template for NIM SDK UI integration (NEChatKit/NEChatUIKit).
license: Complete terms in LICENSE.txt
official: false
---

# NIM SDK iOS Starter Project Generator

此 skill 用于生成一个最小化的 iOS 项目模板，用于指导用户接入网易云信 NIM SDK（带 UI 界面）。

## 触发条件

当用户需要：
- 创建一个空的 iOS 项目用于接入带 UI 界面的 NIM SDK
- 生成包含 Podfile 的项目模板
- 执行 `pod install` 安装 NIM SDK UI 依赖（NEChatKit, NEChatUIKit, NEConversationUIKit）

## 工作流程

### 1. 调用 Python 脚本创建项目

**使用 bundled resource 中的 Python 脚本自动创建项目：**

```bash
python3 ${SKILLS_ROOT:-/Users/yaoxiao/Library/Application\ Support/LobsterAI/SKILLs}/nim-sdk-ios-starter/scripts/create_nim_starter.py <project_name>
```

或者使用当前 skill 目录路径：

```bash
python3 <skill_directory>/scripts/create_nim_starter.py <project_name>
```

脚本会自动：
- 创建最小化 iOS 项目结构（带 SceneDelegate 支持）
- 生成包含正确 pods 的 Podfile（NEChatKit, NEChatUIKit, NEConversationUIKit 10.9.0）
- 自动执行 `pod install`
- 创建必要的 Swift 文件和资源（AppDelegate, SceneDelegate, ViewController, Info.plist）

### 2. 验证安装

确认：
- `Pods/` 目录已创建
- `{ProjectName}.xcworkspace` 文件已生成
- 提示用户使用 `.xcworkspace` 文件打开项目

## 项目文件模板

### AppDelegate.swift
```swift
import UIKit
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
```

### SceneDelegate.swift
```swift
import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = ViewController()
        window?.makeKeyAndVisible()
    }
}
```

### ViewController.swift
```swift
import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white

        // TODO: 添加 NIM SDK UI 接入代码
        // 例如：初始化 NEChatUIKit，展示会话列表等
    }
}
```

## 输出

执行完成后：
1. 告知用户项目已创建成功
2. 提示用户使用 `.xcworkspace` 文件打开项目（不是 `.xcodeproj`）

## 注意事项

- 确保系统已安装 CocoaPods (`sudo gem install cocoapods`)
- 如果 `pod install` 失败，检查网络或尝试 `pod install --repo-update`
- 提醒用户替换 `your_app_key` 为实际的网易云信 App Key
- 此模板使用 SceneDelegate 架构，适用于 iOS 13+
- 在 Apple Silicon Mac 上，模拟器只支持 Rosetta (x86_64)，真机运行不受影响
