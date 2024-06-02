import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import webbrowser
import json
import os

class VRChatLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyLauncherVRC")

        self.profiles = {}
        self.current_profile_name = None
        self.load_profiles()
        self.profile_listbox = tk.Listbox(root)
        self.profile_listbox.grid(row=0, column=5, rowspan=19, padx=5, pady=5)
        self.profile_listbox.bind('<<ListboxSelect>>', self.on_profile_select)

        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=0, padx=5, pady=5)

        tk.Label(root, text="World ID:").grid(row=0, column=0, sticky=tk.W)
        self.world_id_entry = tk.Entry(root, width=50)
        self.world_id_entry.grid(row=0, column=1, columnspan=3)

        tk.Label(root, text="Instance ID:").grid(row=1, column=0, sticky=tk.W)
        self.instance_id_entry = tk.Entry(root, width=50)
        self.instance_id_entry.grid(row=1, column=1, columnspan=3)

        tk.Label(root, text="Instance Type:").grid(row=2, column=0, sticky=tk.W)
        self.instance_type_var = tk.StringVar(root)
        self.instance_type_var.set("public")
        tk.OptionMenu(root, self.instance_type_var, "public", "friends_plus", "friends", "invite_plus", "invite", "group_public", "group_plus", "group").grid(row=2, column=1)

        tk.Label(root, text="Region:").grid(row=3, column=0, sticky=tk.W)
        self.region_entry = tk.StringVar(root)
        self.region_entry.set("us")
        tk.OptionMenu(root, self.region_entry, "us", "use", "eu", "jp").grid(row=3, column=1)

        tk.Label(root, text="User/Group ID (For non-public instances):").grid(row=4, column=0, sticky=tk.W)
        self.group_id_entry = tk.Entry(root, width=50)
        self.group_id_entry.grid(row=4, column=1, columnspan=3)

        self.no_vr_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Desktop Mode (--no-vr)", variable=self.no_vr_var).grid(row=5, column=0, sticky=tk.W)

        tk.Label(root, text="Profile:").grid(row=6, column=0, sticky=tk.W)
        self.profile_entry = tk.Entry(root, width=50)
        self.profile_entry.grid(row=6, column=1, columnspan=3)

        tk.Label(root, text="FPS:").grid(row=7, column=0, sticky=tk.W)
        self.fps_entry = tk.Entry(root, width=50)
        self.fps_entry.grid(row=7, column=1, columnspan=3)

        self.enable_debug_gui_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Enable Debug GUI (--enable-debug-gui)", variable=self.enable_debug_gui_var).grid(row=8, column=0, sticky=tk.W)

        self.enable_sdk_log_levels_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Enable SDK Log Levels (--enable-sdk-log-levels)", variable=self.enable_sdk_log_levels_var).grid(row=9, column=0, sticky=tk.W)

        self.enable_udon_debug_logging_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Enable Udon Debug Logging (--enable-udon-debug-logging)", variable=self.enable_udon_debug_logging_var).grid(row=10, column=0, sticky=tk.W)

        tk.Label(root, text="MIDI Device:").grid(row=11, column=0, sticky=tk.W)
        self.midi_entry = tk.Entry(root, width=50)
        self.midi_entry.grid(row=11, column=1, columnspan=3)

        self.watch_worlds_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Watch Worlds (--watch-worlds)", variable=self.watch_worlds_var).grid(row=12, column=0, sticky=tk.W)

        self.watch_avatars_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Watch Avatars (--watch-avatars)", variable=self.watch_avatars_var).grid(row=13, column=0, sticky=tk.W)

        tk.Label(root, text="Ignore Trackers:").grid(row=14, column=0, sticky=tk.W)
        self.ignore_trackers_entry = tk.Entry(root, width=50)
        self.ignore_trackers_entry.grid(row=14, column=1, columnspan=3)

        self.disable_hw_video_decoding_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Disable HW Video Decoding (--disable-hw-video-decoding)", variable=self.disable_hw_video_decoding_var).grid(row=15, column=0, sticky=tk.W)

        tk.Label(root, text="OSC Settings:").grid(row=16, column=0, sticky=tk.W)
        self.osc_entry = tk.Entry(root, width=50)
        self.osc_entry.grid(row=16, column=1, columnspan=3)

        tk.Label(root, text="Affinity:").grid(row=17, column=0, sticky=tk.W)
        self.affinity_entry = tk.Entry(root, width=50)
        self.affinity_entry.grid(row=17, column=1, columnspan=3)

        tk.Button(root, text="Launch", command=self.launch_vrchat).grid(row=18, column=0, pady=5)
        tk.Button(root, text="Save Profile", command=self.save_profile).grid(row=18,column=1, pady=5)
        tk.Button(root, text="Load Profile", command=self.load_profile).grid(row=18, column=2, pady=5)
        tk.Button(root, text="Edit Command", command=self.edit_command).grid(row=18, column=3, pady=5)
        tk.Button(root, text="New Profile", command=self.new_profile).grid(row=18, column=4, pady=5)  # New Profile button

        self.update_profile_listbox()

    def build_launch_url(self):
        world_id = self.world_id_entry.get()
        instance_id = self.instance_id_entry.get()
        instance_type = self.instance_type_var.get()
        region = self.region_entry.get()
        group_id = self.group_id_entry.get()
        
        instance_types = ["public", "friends_plus", "friends", "invite_plus", "invite", "group_public", "group_plus", "group"]
        
        group_types = ["group_public", "group_plus", "group"]
        group_access_types = {
            "group_public": "public",
            "group_plus": "plus",
            "group": "members",
        }
        "canRequestInvite"
        user_or_group_prefix = ""
        if instance_type in ["group", "group_plus", "group_public"]:
            user_or_group_prefix = "group"
        elif instance_type in ["friends_plus"]:
            user_or_group_prefix = "hidden"
        elif instance_type in ["friends"]:
            user_or_group_prefix = "friends"
        elif instance_type in ["invite_plus", "invite"]:
            user_or_group_prefix = "private"

        instance_type_opts = ""

        if instance_type == "public":
            instance_options = f"{instance_id}~region({region})"
            instance_type_opts = ""
        elif instance_type == "friends_plus":
            instance_options = f"{instance_id}~hidden({group_id})~region({region})"
            instance_type_opts = f"hidden({group_id})~"
        elif instance_type == "friends":
            instance_options = f"{instance_id}~friends({group_id})~region({region})"
            instance_type_opts = f"friends({group_id})~"
        elif instance_type == "invite_plus":
            instance_options = f"{instance_id}~private({group_id})~canRequestInvite~region({region})"
            instance_type_opts = f"private({group_id})~canRequestInvite~"
        elif instance_type == "invite":
            instance_options = f"{instance_id}~private({group_id})~region({region})"
            instance_type_opts = f"private({group_id})~"
        elif instance_type in ["group", "group_plus", "group_public"]:
            instance_options = f"{instance_id}~group({group_id})~groupAccessType({group_access_types[instance_type]})~region({region})"
            instance_type_opts = f"group({group_id})~groupAccessType({group_access_types[instance_type]})~"

        base_url = f"vrchat://launch?ref=PyLauncherVRC&id={world_id}:{instance_id}~{instance_type_opts}region({region})"

        command_line_options = []
        if self.no_vr_var.get():
            command_line_options.append("--no-vr")
        if self.profile_entry.get():
            command_line_options.append(f"--profile=\"{self.profile_entry.get()}\"")
        if self.fps_entry.get():
            command_line_options.append(f"--fps={self.fps_entry.get()}")
        if self.enable_debug_gui_var.get():
            command_line_options.append("--enable-debug-gui")
        if self.enable_sdk_log_levels_var.get():
            command_line_options.append("--enable-sdk-log-levels")
        if self.enable_udon_debug_logging_var.get():
            command_line_options.append("--enable-udon-debug-logging")
        if self.midi_entry.get():
            command_line_options.append(f"--midi={self.midi_entry.get()}")
        if self.watch_worlds_var.get():
            command_line_options.append("--watch-worlds")
        if self.watch_avatars_var.get():
            command_line_options.append("--watch-avatars")
        if self.ignore_trackers_entry.get():
            command_line_options.append(f"--ignore-trackers={self.ignore_trackers_entry.get()}")
        if self.disable_hw_video_decoding_var.get():
            command_line_options.append("--disable-hw-video-decoding")
        if self.osc_entry.get():
            command_line_options.append(f"--osc={self.osc_entry.get()}")
        if self.affinity_entry.get():
            command_line_options.append(f"--affinity={self.affinity_entry.get()}")

        full_command = f"{base_url} " + " ".join(command_line_options)
        return full_command.strip()

    def launch_vrchat(self):
        launch_url = self.build_launch_url()
        webbrowser.open(launch_url)

    def save_profile(self):
        profile_name = simpledialog.askstring("Save Profile", "Enter profile name:")
        if profile_name:
            self.profiles[profile_name] = {
                "world_id": self.world_id_entry.get(),
                "instance_id": self.instance_id_entry.get(),
                "instance_type": self.instance_type_var.get(),
                "region": self.region_entry.get(),
                "group_id": self.group_id_entry.get(),
                "no_vr": self.no_vr_var.get(),
                "profile": self.profile_entry.get(),
                "fps": self.fps_entry.get(),
                "enable_debug_gui": self.enable_debug_gui_var.get(),
                "enable_sdk_log_levels": self.enable_sdk_log_levels_var.get(),
                "enable_udon_debug_logging": self.enable_udon_debug_logging_var.get(),
                "midi": self.midi_entry.get(),
                "watch_worlds": self.watch_worlds_var.get(),
                "watch_avatars": self.watch_avatars_var.get(),
                "ignore_trackers": self.ignore_trackers_entry.get(),
                "disable_hw_video_decoding": self.disable_hw_video_decoding_var.get(),
                "osc": self.osc_entry.get(),
                "affinity": self.affinity_entry.get(),
            }
            self.save_profiles()
            self.update_profile_listbox()

    def load_profile(self):
        profile_name = simpledialog.askstring("Load Profile", "Enter profile name:")
        if profile_name in self.profiles:
            self.set_profile(profile_name)
        else:
            messagebox.showerror("Error", f"No profile named '{profile_name}' found.")

    def set_profile(self, profile_name):
        profile = self.profiles[profile_name]
        self.world_id_entry.delete(0, tk.END)
        self.world_id_entry.insert(0, profile["world_id"])

        self.instance_id_entry.delete(0, tk.END)
        self.instance_id_entry.insert(0, profile["instance_id"])

        self.instance_type_var.set(profile["instance_type"])
        self.region_entry.set(profile["region"])

        self.group_id_entry.delete(0, tk.END)
        self.group_id_entry.insert(0, profile["group_id"])

        self.no_vr_var.set(profile["no_vr"])

        self.profile_entry.delete(0, tk.END)
        self.profile_entry.insert(0, profile["profile"])

        self.fps_entry.delete(0, tk.END)
        self.fps_entry.insert(0, profile["fps"])

        self.enable_debug_gui_var.set(profile["enable_debug_gui"])
        self.enable_sdk_log_levels_var.set(profile["enable_sdk_log_levels"])
        self.enable_udon_debug_logging_var.set(profile["enable_udon_debug_logging"])

        self.midi_entry.delete(0, tk.END)
        self.midi_entry.insert(0, profile["midi"])

        self.watch_worlds_var.set(profile["watch_worlds"])
        self.watch_avatars_var.set(profile["watch_avatars"])

        self.ignore_trackers_entry.delete(0, tk.END)
        self.ignore_trackers_entry.insert(0, profile["ignore_trackers"])

        self.disable_hw_video_decoding_var.set(profile["disable_hw_video_decoding"])

        self.osc_entry.delete(0, tk.END)
        self.osc_entry.insert(0, profile["osc"])

        self.affinity_entry.delete(0, tk.END)
        self.affinity_entry.insert(0, profile["affinity"])

    def load_profiles(self):
        if os.path.exists("profiles.json"):
            with open("profiles.json", "r") as f:
                self.profiles = json.load(f)
        else:
            self.profiles = {}

    def save_profiles(self):
        with open("profiles.json", "w") as f:
            json.dump(self.profiles, f, indent=4)

    def update_profile_listbox(self):
        self.profile_listbox.delete(0, tk.END)
        for profile_name in self.profiles:
            self.profile_listbox.insert(tk.END, profile_name)

    def on_profile_select(self, event):
        selected_index = self.profile_listbox.curselection()
        if selected_index:
            profile_name = self.profile_listbox.get(selected_index[0])
            self.set_profile(profile_name)

    def edit_command(self):
        command = self.build_launch_url()
        edited_command = simpledialog.askstring("Edit Command", "Modify command:", initialvalue=command)
        if edited_command:
            print(f"Edited Command: {edited_command}")

    def new_profile(self):
        self.world_id_entry.delete(0, tk.END)
        self.instance_id_entry.delete(0, tk.END)
        self.instance_type_var.set("public")
        self.region_entry.set("us")
        self.group_id_entry.delete(0, tk.END)
        self.no_vr_var.set(False)
        self.profile_entry.delete(0, tk.END)
        self.fps_entry.delete(0, tk.END)
        self.enable_debug_gui_var.set(False)
        self.enable_sdk_log_levels_var.set(False)
        self.enable_udon_debug_logging_var.set(False)
        self.midi_entry.delete(0, tk.END)
        self.watch_worlds_var.set(False)
        self.watch_avatars_var.set(False)
        self.ignore_trackers_entry.delete(0, tk.END)
        self.disable_hw_video_decoding_var.set(False)
        self.osc_entry.delete(0, tk.END)
        self.affinity_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VRChatLauncherApp(root)
    root.mainloop()
