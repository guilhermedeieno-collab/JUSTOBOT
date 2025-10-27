cask "justobot" do
  version "1.0.0"
  sha256 :no_check

  url "https://github.com/guilhermedeieno-collab/JUSTOBOT/releases/download/v#{version}/JustoBot-#{version}-mac-universal.zip"
  name "JustoBot"
  desc "Sistema de Consulta de Processos Judiciais"
  homepage "https://github.com/guilhermedeieno-collab/JUSTOBOT"

  livecheck do
    url :url
    strategy :github_latest
  end

  auto_updates true

  app "JustoBot.app"

  preflight do
    # Ensure Python dependencies are installed
    system_command "#{staged_path}/JustoBot.app/Contents/Resources/scripts/install_dependencies.sh"
  end

  postflight do
    # Set up Python virtual environment
    system_command "#{appdir}/JustoBot.app/Contents/Resources/scripts/setup_venv.sh"
  end

  uninstall quit: "com.justobot.app",
            delete: "~/Library/Application Support/JustoBot"

  zap trash: [
    "~/Library/Application Support/JustoBot",
    "~/Library/Preferences/com.justobot.app.plist",
    "~/Library/Saved Application State/com.justobot.app.savedState",
    "~/Library/Logs/JustoBot",
  ]
end
