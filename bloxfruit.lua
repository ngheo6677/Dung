-- Blox Fruits Script với Menu
local Player = game.Players.LocalPlayer
local UIS = game:GetService("UserInputService")
local GUI = Instance.new("ScreenGui")
local Frame = Instance.new("Frame")
local AutoFarmButton = Instance.new("TextButton")
local FlyButton = Instance.new("TextButton")
local HitboxToggle = Instance.new("TextButton")
local PlayerSize = 0

-- Tạo GUI
GUI.Parent = Player:WaitForChild("PlayerGui")
Frame.Parent = GUI
Frame.Size = UDim2.new(0, 200, 0, 200)
Frame.Position = UDim2.new(0.5, -100, 0.5, -100)
Frame.BackgroundColor3 = Color3.new(0.2, 0.2, 0.2)

-- Tạo Nút Auto Farm
AutoFarmButton.Parent = Frame
AutoFarmButton.Size = UDim2.new(0, 180, 0, 50)
AutoFarmButton.Position = UDim2.new(0, 10, 0, 10)
AutoFarmButton.Text = "Auto Farm"
AutoFarmButton.BackgroundColor3 = Color3.new(1, 0, 0)

-- Tạo Nút Bay
FlyButton.Parent = Frame
FlyButton.Size = UDim2.new(0, 180, 0, 50)
FlyButton.Position = UDim2.new(0, 10, 0, 70)
FlyButton.Text = "Fly"
FlyButton.BackgroundColor3 = Color3.new(0, 1, 0)

-- Tạo Nút Hitbox
HitboxToggle.Parent = Frame
HitboxToggle.Size = UDim2.new(0, 180, 0, 50)
HitboxToggle.Position = UDim2.new(0, 10, 0, 130)
HitboxToggle.Text = "Toggle Hitbox"
HitboxToggle.BackgroundColor3 = Color3.new(0, 0, 1)

-- Auto Farm
AutoFarmButton.MouseButton1Click:Connect(function()
    while true do
        wait(1)
        for _, fruit in pairs(workspace:GetChildren()) do
            if fruit:IsA("Fruit") then
                Player.Character.HumanoidRootPart.CFrame = fruit.CFrame
                wait(0.5) -- Thời gian để thu thập trái cây
            end
        end
    end
end)

-- Bay
FlyButton.MouseButton1Click:Connect(function()
    local flying = not flying
    if flying then
        local bodyVelocity = Instance.new("BodyVelocity", character.HumanoidRootPart)
        bodyVelocity.Velocity = Vector3.new(0, 50, 0)
        bodyVelocity.MaxForce = Vector3.new(0, math.huge, 0)
        while flying do
            wait()
            bodyVelocity.Velocity = workspace.CurrentCamera.CFrame.LookVector * 50
        end
        bodyVelocity:Destroy()
    end
end)

-- Toggle Hitbox
HitboxToggle.MouseButton1Click:Connect(function()
    PlayerSize = PlayerSize == 0 and 3 or 0
    Player.Character.Humanoid:SetScale(Vector3.new(PlayerSize, PlayerSize, PlayerSize))
end)
