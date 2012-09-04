package {"django":
		ensure => "1.3.1",
		provider => pip;
}

package {"setuptools-git":
		provider => pip;
}

package { "fabric":
	ensure => "0.9.3",
	provider => pip,
}

package { "python-dateutil":
        ensure => "2.1",
        provider => pip,
}

package {"mock":
	provider => pip;
}

